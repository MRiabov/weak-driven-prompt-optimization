import uuid
import time
import dspy
from src.models.domain import (
    PromptCandidate,
    EvaluationResult,
    ModelOutputRecord,
)
from src.evaluation.loaders import DatasetLoader
from src.evaluation.exporter import DatasetExporter
from src.evaluation.metrics import get_evaluator
from src.optimization.optimizer import optimize_baseline, harden_prompt
from src.runner.state import ExperimentStateManager, ExperimentStatus
from src.utils.llm_client import get_llm_client
from src.optimization.modules import QAModule


class Stage1Executor:
    """Executes Stage 1: Baseline optimization using a strong model."""

    def __init__(self, state_manager: ExperimentStateManager, strong_model: str):
        self.state_manager = state_manager
        self.strong_model = strong_model

    def execute(
        self, train_loader: DatasetLoader, benchmark: str, limit: int = 10
    ) -> PromptCandidate:
        self.state_manager.update_status(ExperimentStatus.STAGE_1_RUNNING)

        # Load training data
        trainset = [
            dspy.Example(question=r["question"], answer=r["answer"]).with_inputs(
                "question"
            )
            for r in train_loader.load(benchmark, split="train", limit=limit)
        ]

        # Execute optimization
        candidate = optimize_baseline(trainset, self.strong_model)

        # Save results
        self.state_manager.save_candidate(candidate)
        self.state_manager.increment_iteration()
        self.state_manager.update_status(ExperimentStatus.STAGE_1_COMPLETE)

        return candidate


class Stage2Executor:
    """Executes Stage 2: Hardening the baseline prompt against weak model failures."""

    def __init__(
        self, state_manager: ExperimentStateManager, strong_model: str, weak_model: str
    ):
        self.state_manager = state_manager
        self.strong_model = strong_model
        self.weak_model = weak_model

    def execute(
        self,
        train_loader: DatasetLoader,
        benchmark: str,
        baseline_prompt: PromptCandidate,
        limit: int = 10,
    ) -> PromptCandidate:
        self.state_manager.update_status(ExperimentStatus.STAGE_2_RUNNING)

        # Load training data
        trainset = [
            dspy.Example(question=r["question"], answer=r["answer"]).with_inputs(
                "question"
            )
            for r in train_loader.load(benchmark, split="train", limit=limit)
        ]

        # Execute hardening
        candidate = harden_prompt(
            trainset, baseline_prompt, self.strong_model, self.weak_model
        )

        # Save results
        self.state_manager.save_candidate(candidate)
        self.state_manager.increment_iteration()
        self.state_manager.update_status(ExperimentStatus.STAGE_2_COMPLETE)

        return candidate


class Stage3Executor:
    """Executes Stage 3: Final evaluation of a prompt candidate."""

    def __init__(
        self, state_manager: ExperimentStateManager, exporter: DatasetExporter
    ):
        self.state_manager = state_manager
        self.exporter = exporter

    def execute(
        self,
        test_loader: DatasetLoader,
        benchmark: str,
        candidate: PromptCandidate,
        model_name: str,
        limit: int = 20,
    ) -> EvaluationResult:
        lm = get_llm_client(model_name)
        evaluator_fn = get_evaluator(benchmark)

        # Initialize module with prompt content
        module = QAModule()
        for name, parameter in module.named_predictors():
            parameter.signature = parameter.signature.with_instructions(
                candidate.content
            )

        records = []
        correct_count = 0
        total_count = 0
        start_time = time.time()

        # Run evaluation loop
        with dspy.context(lm=lm):
            for record in test_loader.load(benchmark, split="test", limit=limit):
                total_count += 1
                prediction = module(question=record["question"])

                is_correct, parsed_answer = evaluator_fn(
                    prediction.answer, record["answer"]
                )
                if is_correct:
                    correct_count += 1

                records.append(
                    ModelOutputRecord(
                        output_id=str(uuid.uuid4()),
                        eval_id=candidate.prompt_id,  # Link to candidate for simplicity or use a separate eval_id
                        prompt_id=candidate.prompt_id,
                        model_used=model_name,
                        input_query=record["question"],
                        raw_output=prediction.answer,
                        parsed_answer=parsed_answer,
                        expected_answer=record["answer"],
                        is_correct=is_correct,
                    )
                )

        duration = time.time() - start_time
        accuracy = correct_count / total_count if total_count > 0 else 0.0

        # Persist detailed outputs
        eval_id = str(uuid.uuid4())
        output_dir = str(self.state_manager.base_dir / "outputs")
        dataset_path = self.exporter.persist_outputs(eval_id, iter(records), output_dir)

        # Create and save summary result
        result = EvaluationResult(
            eval_id=eval_id,
            prompt_id=candidate.prompt_id,
            benchmark_name=benchmark,
            model_used=model_name,
            accuracy=accuracy,
            api_cost=0.0,  # Cost tracking not implemented yet
            duration_seconds=duration,
            failed_cases=[r.model_dump() for r in records if not r.is_correct][
                :10
            ],  # Store up to 10 failures
            dataset_path=dataset_path,
        )

        self.state_manager.save_evaluation(result)
        return result

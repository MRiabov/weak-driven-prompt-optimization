import logging
from typing import Optional, Dict, Any

from src.models.domain import (
    ExperimentConfig,
    PromptCandidate,
    PromptStage,
)
from src.runner.state import ExperimentStateManager, ExperimentStatus
from src.runner.executors import Stage1Executor, Stage2Executor, Stage3Executor
from src.evaluation.loaders import DatasetLoader
from src.evaluation.exporter import DatasetExporter
from src.utils.observability import init_langfuse, setup_dspy_tracing

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """
    Central coordinator connecting modular experimental stages.
    """

    def __init__(self, config: ExperimentConfig):
        self.config = config
        # WP05 state manager requires max_budget_iterations
        self.state_manager = ExperimentStateManager(
            experiment_id=config.experiment_id,
            max_budget_iterations=config.budget_iterations,
        )
        self.state_manager.save_config(config)

        # Initialize observability
        self.langfuse_handler = init_langfuse()
        setup_dspy_tracing(self.langfuse_handler)

        self.loader = DatasetLoader()
        self.exporter = DatasetExporter()

        # Initialize executors with correct WP05 signatures
        self.stage1_executor = Stage1Executor(
            state_manager=self.state_manager, strong_model=config.large_model
        )
        self.stage2_executor = Stage2Executor(
            state_manager=self.state_manager,
            strong_model=config.large_model,
            weak_model=config.small_model,
        )
        self.stage3_executor = Stage3Executor(
            state_manager=self.state_manager, exporter=self.exporter
        )

    def run(self) -> Dict[str, Any]:
        """
        Executes the full experiment workflow with resuming capabilities.
        """
        logger.info(f"Starting/Resuming experiment {self.config.experiment_id}")

        baseline_candidate: Optional[PromptCandidate] = None
        hardened_candidate: Optional[PromptCandidate] = None

        # Determine benchmark (using the first one for now as per simple stage logic)
        benchmark = self.config.benchmarks[0] if self.config.benchmarks else "gsm8k"

        # Stage 1: Baseline Optimization
        if self.state_manager.status in [
            ExperimentStatus.NOT_STARTED,
            ExperimentStatus.STAGE_1_RUNNING,
        ]:
            logger.info("Running Stage 1: Baseline Optimization")
            baseline_candidate = self.stage1_executor.execute(
                train_loader=self.loader,
                benchmark=benchmark,
                limit=self.config.data_limit,
            )
        else:
            logger.info(
                "Skipping Stage 1 (already complete). Loading baseline candidate."
            )
            # Find the most recent baseline candidate from storage
            candidates_dir = self.state_manager.base_dir / "candidates"
            for f in candidates_dir.glob("*.json"):
                with open(f, "r") as cf:
                    cand = PromptCandidate.model_validate_json(cf.read())
                    if cand.stage == PromptStage.BASELINE:
                        baseline_candidate = cand
                        break

        # Stage 2: Hardening on Small Model
        if self.state_manager.status in [
            ExperimentStatus.STAGE_1_COMPLETE,
            ExperimentStatus.STAGE_2_RUNNING,
        ]:
            logger.info("Running Stage 2: Hardening Optimization")

            # If we resumed and missed baseline_candidate, we need to load it
            if not baseline_candidate:
                # Attempt to find it - this is a bit heuristic without prompt_id in state
                candidates_dir = self.state_manager.base_dir / "candidates"
                baseline_files = list(candidates_dir.glob("*.json"))
                for f in baseline_files:
                    with open(f, "r") as cf:
                        cand = PromptCandidate.model_validate_json(cf.read())
                        if cand.stage == PromptStage.BASELINE:
                            baseline_candidate = cand
                            break

            if not baseline_candidate:
                raise ValueError(
                    "Baseline candidate is required for Stage 2 but was not found."
                )

            hardened_candidate = self.stage2_executor.execute(
                train_loader=self.loader,
                benchmark=benchmark,
                baseline_prompt=baseline_candidate,
                limit=self.config.data_limit,
            )
        else:
            logger.info(
                "Skipping Stage 2 (already complete). Loading hardened candidate."
            )
            # Same heuristic for loading hardened candidate if we're jumping to Stage 3
            pass

        # Stage 3: Evaluation
        if self.state_manager.status in [
            ExperimentStatus.STAGE_2_COMPLETE,
        ]:
            logger.info("Running Stage 3: Final Evaluation")

            # Load candidates if missing (from resumption)
            if not baseline_candidate or not hardened_candidate:
                candidates_dir = self.state_manager.base_dir / "candidates"
                for f in candidates_dir.glob("*.json"):
                    with open(f, "r") as cf:
                        cand = PromptCandidate.model_validate_json(cf.read())
                        if cand.stage == PromptStage.BASELINE:
                            baseline_candidate = cand
                        elif cand.stage == PromptStage.HARDENED:
                            hardened_candidate = cand

            if not baseline_candidate or not hardened_candidate:
                raise ValueError(
                    "Both baseline and hardened candidates are required for Stage 3."
                )

            # Evaluate baseline on small model (control)
            logger.info(f"Evaluating baseline prompt on {self.config.small_model}...")
            self.stage3_executor.execute(
                test_loader=self.loader,
                benchmark=benchmark,
                candidate=baseline_candidate,
                model_name=self.config.small_model,
                limit=self.config.data_limit,
            )

            # Evaluate hardened on small model (experiment)
            logger.info(f"Evaluating hardened prompt on {self.config.small_model}...")
            self.stage3_executor.execute(
                test_loader=self.loader,
                benchmark=benchmark,
                candidate=hardened_candidate,
                model_name=self.config.small_model,
                limit=self.config.data_limit,
            )

            # Evaluate baseline on large model (control-large)
            logger.info(f"Evaluating baseline prompt on {self.config.large_model}...")
            self.stage3_executor.execute(
                test_loader=self.loader,
                benchmark=benchmark,
                candidate=baseline_candidate,
                model_name=self.config.large_model,
                limit=self.config.data_limit,
            )

            # Evaluate hardened on large model (experiment-large)
            logger.info(f"Evaluating hardened prompt on {self.config.large_model}...")
            self.stage3_executor.execute(
                test_loader=self.loader,
                benchmark=benchmark,
                candidate=hardened_candidate,
                model_name=self.config.large_model,
                limit=self.config.data_limit,
            )

            self.state_manager.update_status(ExperimentStatus.COMPLETE)
        else:
            logger.info("Skipping Stage 3 or already complete.")

        return {
            "status": self.state_manager.status.value,
            "experiment_id": self.config.experiment_id,
        }

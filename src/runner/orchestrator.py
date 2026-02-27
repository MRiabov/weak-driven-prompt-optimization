import logging
from typing import Optional, Dict, Any

from src.models.domain import ExperimentConfig, PromptCandidate, EvaluationResult
from src.runner.state import ExperimentStateManager, ExperimentState
from src.runner.executors import Stage1Executor, Stage2Executor, Stage3Executor
from src.utils.observability import init_langfuse, setup_dspy_tracing

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """
    Central coordinator connecting modular experimental stages.
    """

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.state_manager = ExperimentStateManager(experiment_id=config.experiment_id)

        # Initialize observability
        self.langfuse_handler = init_langfuse()
        setup_dspy_tracing(self.langfuse_handler)

        # Initialize executors
        self.stage1_executor = Stage1Executor(state_manager=self.state_manager)
        self.stage2_executor = Stage2Executor(state_manager=self.state_manager)
        self.stage3_executor = Stage3Executor(state_manager=self.state_manager)

    def run(self) -> Dict[str, Any]:
        """
        Executes the full experiment workflow with resuming capabilities.
        """
        logger.info(f"Starting/Resuming experiment {self.config.experiment_id}")

        current_state = self.state_manager.get_current_state()

        baseline_candidate: Optional[PromptCandidate] = None
        hardened_candidate: Optional[PromptCandidate] = None

        # Stage 1: Baseline Optimization
        if current_state in [
            ExperimentState.NOT_STARTED,
            ExperimentState.STAGE_1_RUNNING,
        ]:
            logger.info("Running Stage 1: Baseline Optimization")
            self.state_manager.update_state(ExperimentState.STAGE_1_RUNNING)
            baseline_candidate = self.stage1_executor.run(self.config)
            self.state_manager.save_checkpoint(
                "baseline_candidate", baseline_candidate.model_dump()
            )
            self.state_manager.update_state(ExperimentState.STAGE_1_COMPLETE)
        else:
            logger.info(
                "Skipping Stage 1 (already complete). Loading baseline candidate."
            )
            baseline_candidate_data = self.state_manager.load_checkpoint(
                "baseline_candidate"
            )
            if baseline_candidate_data:
                baseline_candidate = PromptCandidate(**baseline_candidate_data)

        # Stage 2: Hardening on Small Model
        current_state = self.state_manager.get_current_state()
        if current_state in [
            ExperimentState.STAGE_1_COMPLETE,
            ExperimentState.STAGE_2_RUNNING,
        ]:
            logger.info("Running Stage 2: Hardening Optimization")
            self.state_manager.update_state(ExperimentState.STAGE_2_RUNNING)
            # Failsafe check
            if not baseline_candidate:
                raise ValueError(
                    "Baseline candidate is required for Stage 2 but was not found."
                )

            hardened_candidate = self.stage2_executor.run(
                self.config, baseline_candidate
            )
            self.state_manager.save_checkpoint(
                "hardened_candidate", hardened_candidate.model_dump()
            )
            self.state_manager.update_state(ExperimentState.STAGE_2_COMPLETE)
        else:
            logger.info(
                "Skipping Stage 2 (already complete). Loading hardened candidate."
            )
            hardened_candidate_data = self.state_manager.load_checkpoint(
                "hardened_candidate"
            )
            if hardened_candidate_data:
                hardened_candidate = PromptCandidate(**hardened_candidate_data)

        # Stage 3: Evaluation
        current_state = self.state_manager.get_current_state()
        if current_state in [
            ExperimentState.STAGE_2_COMPLETE,
            ExperimentState.STAGE_3_RUNNING,
        ]:
            logger.info("Running Stage 3: Final Evaluation")
            self.state_manager.update_state(ExperimentState.STAGE_3_RUNNING)

            if not baseline_candidate or not hardened_candidate:
                raise ValueError(
                    "Both baseline and hardened candidates are required for Stage 3."
                )

            # Evaluate baseline
            logger.info("Evaluating baseline prompt...")
            baseline_result = self.stage3_executor.run(self.config, baseline_candidate)
            self.state_manager.save_checkpoint(
                "baseline_result", baseline_result.model_dump()
            )

            # Evaluate hardened
            logger.info("Evaluating hardened prompt...")
            hardened_result = self.stage3_executor.run(self.config, hardened_candidate)
            self.state_manager.save_checkpoint(
                "hardened_result", hardened_result.model_dump()
            )

            self.state_manager.update_state(ExperimentState.EXPERIMENT_COMPLETE)
        else:
            logger.info("Skipping Stage 3. Experiment is already complete.")

        return {
            "status": self.state_manager.get_current_state().value,
            "experiment_id": self.config.experiment_id,
        }

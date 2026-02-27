from enum import Enum
import json
from pathlib import Path
from typing import Optional
from src.models.domain import PromptCandidate, EvaluationResult, ExperimentConfig


class ExperimentStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    STAGE_1_RUNNING = "STAGE_1_RUNNING"
    STAGE_1_COMPLETE = "STAGE_1_COMPLETE"
    STAGE_2_RUNNING = "STAGE_2_RUNNING"
    STAGE_2_COMPLETE = "STAGE_2_COMPLETE"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class ExperimentStateManager:
    def __init__(
        self,
        experiment_id: str,
        max_budget_iterations: int,
        base_dir: str = ".checkpoints",
    ):
        self.experiment_id = experiment_id
        self.max_budget_iterations = max_budget_iterations
        self.current_iterations = 0
        self.status = ExperimentStatus.NOT_STARTED
        self.base_dir = Path(base_dir) / experiment_id
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._state_file = self.base_dir / "state.json"

        # Load existing state if it exists
        self.load_state()

    def can_continue_optimization(self) -> bool:
        """Returns True if the optimization budget has not been exceeded."""
        return self.current_iterations < self.max_budget_iterations

    def update_status(self, status: ExperimentStatus):
        """Updates the experiment status and persists the change."""
        self.status = status
        self.save_state()

    def increment_iteration(self):
        """Increments the iteration count and persists the change."""
        self.current_iterations += 1
        self.save_state()

    def save_state(self):
        """Saves the current experiment metadata to disk."""
        state = {
            "experiment_id": self.experiment_id,
            "max_budget_iterations": self.max_budget_iterations,
            "current_iterations": self.current_iterations,
            "status": self.status.value,
        }
        self._atomic_write(self._state_file, json.dumps(state, indent=2))

    def load_state(self):
        """Loads experiment metadata from disk if available."""
        if self._state_file.exists():
            with open(self._state_file, "r") as f:
                state = json.load(f)
                # We prioritize the loaded max_budget_iterations unless it's fundamentally different
                # In a real app we might want more complex logic here.
                self.current_iterations = state.get("current_iterations", 0)
                self.status = ExperimentStatus(
                    state.get("status", ExperimentStatus.NOT_STARTED.value)
                )
                if "max_budget_iterations" in state:
                    self.max_budget_iterations = state["max_budget_iterations"]

    def save_candidate(self, candidate: PromptCandidate):
        """Checkpoints a PromptCandidate to disk."""
        candidate_dir = self.base_dir / "candidates"
        candidate_dir.mkdir(exist_ok=True)
        file_path = candidate_dir / f"{candidate.prompt_id}.json"
        self._atomic_write(file_path, candidate.model_dump_json(indent=2))

    def load_candidate(self, prompt_id: str) -> PromptCandidate:
        """Loads a PromptCandidate from disk."""
        file_path = self.base_dir / "candidates" / f"{prompt_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Candidate {prompt_id} not found at {file_path}")
        with open(file_path, "r") as f:
            return PromptCandidate.model_validate_json(f.read())

    def save_evaluation(self, evaluation: EvaluationResult):
        """Checkpoints an EvaluationResult to disk."""
        eval_dir = self.base_dir / "evaluations"
        eval_dir.mkdir(exist_ok=True)
        file_path = eval_dir / f"{evaluation.eval_id}.json"
        self._atomic_write(file_path, evaluation.model_dump_json(indent=2))

    def load_evaluation(self, eval_id: str) -> EvaluationResult:
        """Loads an EvaluationResult from disk."""
        file_path = self.base_dir / "evaluations" / f"{eval_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Evaluation {eval_id} not found at {file_path}")
        with open(file_path, "r") as f:
            return EvaluationResult.model_validate_json(f.read())

    def save_config(self, config: ExperimentConfig):
        """Saves the experiment configuration to disk."""
        config_file = self.base_dir / "config.json"
        self._atomic_write(config_file, config.model_dump_json(indent=2))

    def _atomic_write(self, file_path: Path, content: str):
        """Writes content to a file atomically by using a temporary file and renaming it."""
        temp_path = file_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            f.write(content)
        temp_path.replace(file_path)

import json
import logging
from pathlib import Path
from typing import List, Optional

from src.models.domain import (
    EvaluationResult,
    PromptCandidate,
    PromptStage,
    ExperimentConfig,
)

logger = logging.getLogger(__name__)


class ReportingEngine:
    def __init__(self, experiment_id: str, base_dir: str = ".checkpoints"):
        self.experiment_id = experiment_id
        self.exp_dir = Path(base_dir) / experiment_id

    def _load_json(self, path: Path) -> Optional[dict]:
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load {path}: {e}")
            return None

    def load_config(self) -> Optional[ExperimentConfig]:
        config_path = self.exp_dir / "config.json"
        data = self._load_json(config_path)
        if data:
            return ExperimentConfig(**data)
        return None

    def load_prompts(self) -> List[PromptCandidate]:
        prompts = []
        prompts_dir = self.exp_dir / "candidates"
        if not prompts_dir.exists():
            return prompts
        for p in prompts_dir.glob("*.json"):
            data = self._load_json(p)
            if data:
                prompts.append(PromptCandidate(**data))
        return prompts

    def load_evaluations(self) -> List[EvaluationResult]:
        evals = []
        evals_dir = self.exp_dir / "evaluations"
        if not evals_dir.exists():
            return evals
        for p in evals_dir.glob("*.json"):
            data = self._load_json(p)
            if data:
                evals.append(EvaluationResult(**data))
        return evals

    def generate_report(self) -> str:
        config = self.load_config()
        prompts = self.load_prompts()
        evals = self.load_evaluations()

        baseline_prompt_ids = {
            p.prompt_id for p in prompts if p.stage == PromptStage.BASELINE
        }
        hardened_prompt_ids = {
            p.prompt_id for p in prompts if p.stage == PromptStage.HARDENED
        }

        baseline_evals = [e for e in evals if e.prompt_id in baseline_prompt_ids]
        hardened_evals = [e for e in evals if e.prompt_id in hardened_prompt_ids]

        # Fallback if prompt stage data is missing
        if not baseline_evals and evals:
            baseline_evals = [
                e
                for e in evals
                if getattr(e, "prompt_id", "").lower().startswith("baseline")
            ]
        if not hardened_evals and evals:
            hardened_evals = [
                e for e in evals if "hardened" in getattr(e, "prompt_id", "").lower()
            ]

        def agg_metrics(eval_list: List[EvaluationResult]) -> dict:
            if not eval_list:
                return {"accuracy": 0.0, "cost": 0.0, "duration": 0.0, "count": 0}
            acc = sum(e.accuracy for e in eval_list) / len(eval_list)
            cost = sum(e.api_cost for e in eval_list)
            dur = sum(e.duration_seconds for e in eval_list)
            return {
                "accuracy": acc,
                "cost": cost,
                "duration": dur,
                "count": len(eval_list),
            }

        base_metrics = agg_metrics(baseline_evals)
        hard_metrics = agg_metrics(hardened_evals)

        acc_diff = hard_metrics["accuracy"] - base_metrics["accuracy"]
        cost_diff = (
            (hard_metrics["cost"] - base_metrics["cost"])
            / max(base_metrics["cost"], 0.0001)
            * 100
        )
        dur_diff = (
            (hard_metrics["duration"] - base_metrics["duration"])
            / max(base_metrics["duration"], 0.0001)
            * 100
        )

        report = [
            f"# Experiment Report: {self.experiment_id}",
            "",
            "## Configuration Used",
            f"- Large Model: {config.large_model if config else 'N/A'}",
            f"- Small Model: {config.small_model if config else 'N/A'}",
            f"- Benchmarks: {', '.join(config.benchmarks) if config else 'N/A'}",
            f"- Budget Iterations: {config.budget_iterations if config else 'N/A'}",
            "",
            "## Baseline Performance",
            f"- Accuracy: {base_metrics['accuracy']:.2%}",
            f"- Total Cost: ${base_metrics['cost']:.4f}",
            f"- Duration: {base_metrics['duration']:.2f}s",
            f"- Evaluations Count: {base_metrics['count']}",
            "",
            "## Hardened Performance",
            f"- Accuracy: {hard_metrics['accuracy']:.2%}",
            f"- Total Cost: ${hard_metrics['cost']:.4f}",
            f"- Duration: {hard_metrics['duration']:.2f}s",
            f"- Evaluations Count: {hard_metrics['count']}",
            "",
            "## Comparison",
            f"- Accuracy Delta: {'+' if acc_diff > 0 else ''}{acc_diff:.2%}",
            f"- Cost Delta: {'+' if cost_diff > 0 else ''}{cost_diff:.2f}%",
            f"- Duration Delta: {'+' if dur_diff > 0 else ''}{dur_diff:.2f}%",
            "",
            "## Conclusion",
        ]

        if acc_diff > 0:
            report.append(
                "The weak-hardened prompt performed better than the baseline in terms of accuracy."
            )
        elif acc_diff < 0:
            report.append(
                "The weak-hardened prompt performed worse than the baseline in terms of accuracy."
            )
        else:
            if base_metrics["count"] == 0 and hard_metrics["count"] == 0:
                report.append("No evaluation data found. Cannot draw conclusions.")
            else:
                report.append(
                    "The weak-hardened prompt performed identically to the baseline."
                )

        return "\n".join(report)

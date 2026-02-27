# Interfaces

While this is a batch CLI application rather than a web service, the internal interfaces must adhere to strict schemas via Pydantic.

## Experiment Runner Interface

```python
from typing import Iterator

class ExperimentRunner:
    def run_baseline(self, config: ExperimentConfig) -> PromptCandidate:
        """Stage 1: Optimizes prompt on the large model."""
        pass
        
    def run_hardening(self, config: ExperimentConfig, baseline_prompt: PromptCandidate) -> PromptCandidate:
        """Stage 2: Optimizes prompt on the weak model."""
        pass
        
    def evaluate(self, config: ExperimentConfig, prompt: PromptCandidate, model: str) -> EvaluationResult:
        """Stage 3/Eval: Evaluates a prompt on a specific model."""
        pass

class DatasetExporter:
    def persist_outputs(self, eval_id: str, records: Iterator[ModelOutputRecord], output_dir: str) -> str:
        """Persists the model output records to a dataset format (e.g., JSONL) and returns the file path."""
        pass
```
# Data Model: Weak-Driven Prompt Optimization

## Core Entities

### ExperimentConfig
- `experiment_id` (String): Unique identifier for the run.
- `large_model` (String): e.g., "arcee-ai/trinity-large-preview:free".
- `small_model` (String): e.g., "stepfun/step-3.5-flash:free".
- `benchmarks` (List[String]): e.g., ["FRONTIERMATH", "SuperGPQA", "tau^2-Bench"].
- `budget_iterations` (Integer): Max iterations per stage.

### PromptCandidate
- `prompt_id` (String): Unique identifier.
- `stage` (Enum): BASELINE (Large), HARDENED (Small).
- `content` (String): The actual instruction string.
- `parent_prompt_id` (Optional[String]): For tracking lineage.

### EvaluationResult
- `eval_id` (String): Unique identifier.
- `prompt_id` (String): Reference to PromptCandidate.
- `benchmark_name` (String): Name of the dataset.
- `model_used` (String): Model used for evaluation.
- `accuracy` (Float): Score achieved.
- `api_cost` (Float): Total cost of evaluation.
- `duration_seconds` (Float): Time taken.
- `failed_cases` (List[Dict]): Examples where the prompt failed (used for GEPA reflection).
- `dataset_path` (Optional[String]): File path to the persisted model outputs for this evaluation.

### ModelOutputRecord
- `output_id` (String): Unique identifier for the output record.
- `eval_id` (String): Reference to the EvaluationResult this belongs to.
- `prompt_id` (String): Reference to the PromptCandidate used.
- `model_used` (String): The model that generated the output.
- `input_query` (String): The question/prompt sent to the model.
- `raw_output` (String): The exact string returned by the LLM.
- `parsed_answer` (String): The extracted answer used for metric calculation.
- `expected_answer` (String): The ground truth answer from the benchmark.
- `is_correct` (Boolean): Whether the parsed answer matched the expected answer.
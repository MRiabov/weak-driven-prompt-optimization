---
work_package_id: WP01
title: Foundation and Models
lane: "doing"
dependencies: []
base_branch: main
base_commit: fcc593602b6dcaf06b36696cca72738e8d011192
created_at: '2026-02-27T10:01:29.830373+00:00'
subtasks: [T001, T002, T003]
requirement_refs: [FR-001, FR-003]
shell_pid: "852409"
agent: "Gemini"
---

# Work Package Prompt: WP01 - Foundation and Models

## Context & Objective
Set up the core project infrastructure, dependencies, and data schemas necessary for the Weak-Driven Prompt Optimization experiment. This establishes the structural contract (Pydantic models) and the external client connections (Langfuse, OpenRouter) that the rest of the application will rely on.

## Subtasks & Detailed Guidance

### Subtask T001: Set up project environment
- **Purpose**: Initialize the Python environment and dependencies.
- **Steps**:
  1. Configure `pyproject.toml` or `requirements.txt` with the following minimum dependencies:
     - `python = "^3.12"`
     - `dspy-ai`
     - `langfuse`
     - `pydantic`
     - `datasets` (HuggingFace)
     - `openai` (for OpenRouter compatibility)
     - `pyyaml`
  2. Create the base directory structure (`src/models`, `src/utils`, `src/optimization`, `src/evaluation`).
- **Files**: `pyproject.toml` or `requirements.txt`, basic source directories.
- **Parallel?**: No.
- **Notes**: Must ensure strict schema validation using Pydantic as per the constitution.

### Subtask T002: Implement Pydantic domain models
- **Purpose**: Define strict schemas for configuration, states, and results to guarantee data integrity across the pipeline.
- **Steps**:
  1. Create `src/models/domain.py`.
  2. Implement `ExperimentConfig` (large_model, small_model, benchmarks, budget_iterations).
  3. Implement `PromptCandidate` (prompt_id, stage, content, parent_prompt_id).
  4. Implement `EvaluationResult` (eval_id, prompt_id, benchmark_name, model_used, accuracy, api_cost, duration_seconds, failed_cases, dataset_path).
  5. Implement `ModelOutputRecord` (output_id, eval_id, prompt_id, model_used, input_query, raw_output, parsed_answer, expected_answer, is_correct).
- **Files**: `src/models/domain.py`
- **Parallel?**: No.
- **Notes**: Validation logic must ensure these models are correctly initialized.

### Subtask T003: Configure Langfuse tracing and OpenRouter clients
- **Purpose**: Establish the utility layer for observability and model access.
- **Steps**:
  1. Create `src/utils/observability.py`.
  2. Implement initialization logic for Langfuse using environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`).
  3. Ensure the Langfuse callback handler can be cleanly attached to DSPy runs.
  4. Create `src/utils/llm_client.py`.
  5. Configure the OpenRouter client (via OpenAI SDK/DSPy integration) using the `OPENROUTER_API_KEY`.
- **Files**: `src/utils/observability.py`, `src/utils/llm_client.py`
- **Parallel?**: No.
- **Notes**: Client initialization handles missing environment variables gracefully (e.g., throwing a clear error).

## Risks & Review Guidance
- **Schema strictness**: Ensure all fields in Pydantic models map exactly to the data-model.md specification.
- **Client configuration**: DSPy has specific ways of registering language models. Ensure the OpenRouter setup is fully compatible with DSPy's `dspy.LM` or equivalent setup.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T10:01:30Z – Gemini – shell_pid=852409 – lane=doing – Assigned agent via workflow command

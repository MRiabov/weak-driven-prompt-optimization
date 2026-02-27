---
work_package_id: WP02
title: Data Loading and Evaluation Harness
lane: "for_review"
dependencies: [WP01]
subtasks: [T004, T005, T006]
agent: "gemini-cli"
requirement_refs: [FR-002, FR-005]
---

# Work Package Prompt: WP02 - Data Loading and Evaluation Harness

## Context & Objective
Implement the data pipeline required to evaluate the models. This includes streaming benchmarks from HuggingFace, executing evaluation metrics on the model outputs, and persisting the raw outputs to disk for downstream analysis.

## Subtasks & Detailed Guidance

### Subtask T004: Implement HuggingFace dataset streaming loaders
- **Purpose**: Load FRONTIERMATH, SuperGPQA, and tau^2-Bench efficiently without large local downloads.
- **Steps**:
  1. Create `src/evaluation/loaders.py`.
  2. Implement a unified interface or factory to load the specified datasets in streaming mode (`streaming=True`).
  3. Standardize the yielded records into a common dictionary format expected by the evaluators (e.g., `{"question": "...", "answer": "..."}`).
- **Files**: `src/evaluation/loaders.py`
- **Parallel?**: Yes, independent of WP03.

### Subtask T005: Implement metric evaluation functions
- **Purpose**: Score the generated model outputs against the expected ground truth.
- **Steps**:
  1. Create `src/evaluation/metrics.py`.
  2. Implement exact match and regex-based parsing functions appropriate for math and QA benchmarks.
  3. The function must accept `raw_output` and `expected_answer`, and return a boolean indicating correctness and the `parsed_answer` extracted from the output.
- **Files**: `src/evaluation/metrics.py`

### Subtask T006: Implement `DatasetExporter` for JSONL output
- **Purpose**: Save every LLM generation and its correctness evaluation to a local file.
- **Steps**:
  1. Create `src/evaluation/exporter.py`.
  2. Implement the `DatasetExporter` interface defined in `contracts/interfaces.md`.
  3. It should accept an iterator of `ModelOutputRecord` (from WP01) and write them line-by-line to a `.jsonl` file.
  4. The output path should be dynamically generated based on the `eval_id`.
- **Files**: `src/evaluation/exporter.py`

## Risks & Review Guidance
- **Streaming limitations**: Ensure the streaming implementation handles network interruptions gracefully or limits the dataset size effectively based on `budget_iterations` or a sampling limit.
- **Metric robustness**: Evaluation metrics are notoriously brittle. Ensure the parsing logic is robust enough to handle varying formats returned by different models.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T10:18:53Z – gemini-cli – lane=in_progress – Moved to in_progress
- 2026-02-27T10:21:34Z – gemini-cli – lane=for_review – Moved to for_review

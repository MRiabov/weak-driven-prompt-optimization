---
work_package_id: WP09
title: Integration Testing
lane: "for_review"
dependencies: [WP07, WP08]
base_branch: main
base_commit: 3b7d712438cf26e949293e53c1626a5c2a737036
created_at: '2026-02-27T14:34:34.557386+00:00'
subtasks: [T023, T024]
agent: Antigravity
shell_pid: '922104'
requirement_refs: [FR-004]
---

# Work Package Prompt: WP09 - Integration Testing

## Context & Objective
Following the project constitution, we reject unit testing in favor of full-workflow black-box integration tests. This package implements a mock LLM provider so the entire orchestration pipeline and CLI can be run locally without incurring API costs.

## Subtasks & Detailed Guidance

### Subtask T023: Implement mock LLM client for DSPy
- **Purpose**: Prevent actual network calls to OpenRouter during testing.
- **Steps**:
  1. Create `tests/mock_llm.py`.
  2. Implement a dummy LLM class that inherits from DSPy's base LM class.
  3. It must return predictable responses based on the input prompts, simulating both "success" and "failure" scenarios to test the optimizer's logic.
- **Files**: `tests/mock_llm.py`

### Subtask T024: Write end-to-end integration tests
- **Purpose**: Verify the entire experimental framework executes successfully from CLI to Report.
- **Steps**:
  1. Create `tests/integration/test_pipeline.py`.
  2. Use `pytest`.
  3. Set up a test that provides a mock configuration, overrides the LLM client with the mock, and triggers the `run-experiment` CLI command via `click.testing` or `subprocess`.
  4. Assert that the pipeline completes, state checkpoints are created, and the `report` command generates valid output.
- **Files**: `tests/integration/test_pipeline.py`

## Risks & Review Guidance
- **Mock fidelity**: Ensure the mock LLM returns data formatted correctly enough for DSPy's parsers to handle, otherwise the optimization loops will crash internally before completing the test.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T14:34:34Z – Antigravity – shell_pid=922104 – lane=doing – Assigned agent via workflow command
- 2026-02-27T15:15:36Z – Antigravity – shell_pid=922104 – lane=for_review – Ready for review: Implemented mock LLM client (tests/mock_llm.py) and end-to-end integration test (tests/integration/test_pipeline.py). Test exercises the full pipeline from CLI to report generation using mocked LLMs and datasets.

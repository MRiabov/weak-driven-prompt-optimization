---
work_package_id: "WP06"
title: "Integration Testing"
lane: "planned"
requirement_refs: ["FR-004"]
dependencies: ["WP05"]
subtasks: ["T016", "T017"]
---

# Work Package Prompt: WP06 - Integration Testing

## Context & Objective
Following the project constitution, we reject unit testing in favor of full-workflow black-box integration tests. This package implements a mock LLM provider so the entire pipeline can be run locally without incurring API costs.

## Subtasks & Detailed Guidance

### Subtask T016: Implement mock LLM client for DSPy
- **Purpose**: Prevent actual network calls to OpenRouter during testing.
- **Steps**:
  1. Create `tests/mock_llm.py`.
  2. Implement a dummy LLM class that inherits from DSPy's base LM class or intercepts the OpenAI client.
  3. It must return predictable responses based on the input prompts, simulating both "success" and "failure" scenarios to test the optimizer's logic.
- **Files**: `tests/mock_llm.py`

### Subtask T017: Write end-to-end integration tests
- **Purpose**: Verify the entire experimental framework executes successfully.
- **Steps**:
  1. Create `tests/integration/test_pipeline.py`.
  2. Use `pytest`.
  3. Set up a test that provides a mock configuration, uses the mock LLM, and triggers the CLI's `run-experiment` function programmatically or triggers the `ExperimentRunner` directly.
  4. Assert that:
     - Three stages are executed.
     - Output JSONL files are created.
     - A final report can be generated successfully.
- **Files**: `tests/integration/test_pipeline.py`

## Risks & Review Guidance
- **Mock fidelity**: Ensure the mock LLM returns data formatted correctly enough for DSPy's parsers to handle, otherwise the optimization loops will crash internally before completing the test.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
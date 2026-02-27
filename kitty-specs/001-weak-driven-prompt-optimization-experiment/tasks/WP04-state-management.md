---
work_package_id: WP04
title: State Management and Checkpointing
lane: "doing"
dependencies: [WP01]
base_branch: main
base_commit: 6fa69bcfbf7d3e1771e71d17dadd64aa7844ba38
created_at: '2026-02-27T11:00:53.316779+00:00'
subtasks: [T010, T011, T012]
agent: "Antigravity"
shell_pid: "922104"
requirement_refs: [FR-005, FR-006]
---

# Work Package Prompt: WP04 - State Management and Checkpointing

## Context & Objective
Because experiments use expensive external API calls (OpenRouter) and can take a long time, the application needs a robust state manager. This ensures we can pause, resume, and track the optimization budget, fulfilling the requirement that API costs and iterations are strictly managed and protected from unexpected crashes.

## Subtasks & Detailed Guidance

### Subtask T010: Implement `ExperimentState` manager
- **Purpose**: A centralized service to track the current state of an ongoing experiment.
- **Steps**:
  1. Create `src/runner/state.py`.
  2. Implement `ExperimentStateManager` class initialized with an `experiment_id`.
  3. It should track which stage the experiment is currently on (e.g., `NOT_STARTED`, `STAGE_1_RUNNING`, `STAGE_1_COMPLETE`, etc.).
- **Files**: `src/runner/state.py`
- **Parallel?**: No.

### Subtask T011: Implement budget iteration tracking
- **Purpose**: Prevent runaway API usage and fulfill FR-006 for budget-equivalent comparisons.
- **Steps**:
  1. In `ExperimentStateManager`, add tracking for `current_iterations` and `max_budget_iterations`.
  2. Provide a method `can_continue_optimization()` that returns false if the budget is exhausted.
- **Files**: `src/runner/state.py`

### Subtask T012: Implement save/load checkpoints for models
- **Purpose**: Persist Pydantic domain models to disk to enable resumption.
- **Steps**:
  1. Implement methods in the state manager to serialize `PromptCandidate` and `EvaluationResult` objects to JSON files within an experiment-specific directory (`.checkpoints/{experiment_id}/`).
  2. Implement load methods that read these JSON files and reinstantiate the Pydantic objects.
- **Files**: `src/runner/state.py`

## Risks & Review Guidance
- **Atomicity**: Ensure file writes for checkpoints are atomic (e.g., write to a `.tmp` file and rename) to prevent corrupted states if a crash happens exactly during the save operation.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T11:00:53Z – gemini-cli – shell_pid=906016 – lane=doing – Assigned agent via workflow command
- 2026-02-27T11:01:48Z – gemini-cli – shell_pid=906016 – lane=for_review – Implemented ExperimentStateManager with budget tracking and atomic model checkpointing. Verified with integration tests.
- 2026-02-27T11:23:22Z – Antigravity – shell_pid=922104 – lane=doing – Started review via workflow command

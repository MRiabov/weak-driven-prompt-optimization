---
work_package_id: WP06
title: Pipeline Orchestrator
lane: "doing"
dependencies: [WP05]
base_branch: main
base_commit: 46dc0f7eb87f4a5febdce5ba4be1d51fb44b4815
created_at: '2026-02-27T12:02:11.479324+00:00'
subtasks: [T016, T017]
requirement_refs: [FR-004]
shell_pid: "922104"
---

# Work Package Prompt: WP06 - Pipeline Orchestrator

## Context & Objective
With all individual stages, datasets, and state managers implemented, we need a central coordinator. The `ExperimentRunner` connects these modular pieces, passing the output of one executor as the input to the next, fulfilling the multi-stage requirement.

## Subtasks & Detailed Guidance

### Subtask T016: Implement the `ExperimentRunner`
- **Purpose**: Serve as the high-level API for triggering a full experiment.
- **Steps**:
  1. Create `src/runner/orchestrator.py`.
  2. Implement `ExperimentRunner(config: ExperimentConfig)`.
  3. Initialize the observability layer, `ExperimentStateManager`, and the executors from WP05.
- **Files**: `src/runner/orchestrator.py`
- **Parallel?**: No.

### Subtask T017: Wire transitions (Stage 1 -> Stage 2 -> Stage 3)
- **Purpose**: Define the actual sequence of operations.
- **Steps**:
  1. Implement a method `run()`.
  2. Check state manager to see if resuming.
  3. If Stage 1 not complete: Call `Stage1Executor`, save result.
  4. If Stage 2 not complete: Call `Stage2Executor` with Stage 1 result, save result.
  5. If Stage 3 not complete: Call `Stage3Executor` on *both* the baseline prompt (for control) and the hardened prompt (for the experiment test).
  6. Ensure all outputs are finalized and state is marked `EXPERIMENT_COMPLETE`.
- **Files**: `src/runner/orchestrator.py`

## Risks & Review Guidance
- **Resumption Logic**: Test edge cases where the script is killed midway through Stage 2. The orchestrator must gracefully load the Stage 1 candidate and resume Stage 2 without re-running Stage 1.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.

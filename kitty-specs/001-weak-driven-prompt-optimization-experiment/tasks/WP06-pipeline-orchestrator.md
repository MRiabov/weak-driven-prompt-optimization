---
work_package_id: WP06
title: Pipeline Orchestrator
lane: "doing"
dependencies: [WP05]
base_branch: main
base_commit: 46dc0f7eb87f4a5febdce5ba4be1d51fb44b4815
created_at: '2026-02-27T12:02:11.479324+00:00'
subtasks: [T016, T017]
agent: "Antigravity"
shell_pid: "922104"
requirement_refs: [FR-004]
review_status: "has_feedback"
reviewed_by: "MRiabov"
review_feedback_file: "/tmp/spec-kitty-review-feedback-WP06.md"
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

## Review Feedback

**Reviewed by**: MRiabov
**Status**: ❌ Changes Requested
**Date**: 2026-02-27
**Feedback file**: `/tmp/spec-kitty-review-feedback-WP06.md`

### Review Feedback for WP06 - Pipeline Orchestrator

The implementation of `ExperimentRunner` in `src/runner/orchestrator.py` has several critical issues that prevent it from being functional:

1. **Missing Dependencies**: The files `src/runner/state.py` and `src/runner/executors.py` are imported but do not exist in the WP06 workspace. These should have been inherited from WP05.
2. **API Mismatch**: The usage of `ExperimentStateManager` in `orchestrator.py` does not match the implementation found in the `WP05` branch.
    - `orchestrator.py` expects `ExperimentStateManager(experiment_id=config.experiment_id)`.
    - `WP05`'s `state.py` implements `ExperimentStateManager(experiment_id, max_budget_iterations, base_dir)`.
    - `orchestrator.py` calls `get_current_state()`, `update_state()`, `save_checkpoint()`, and `load_checkpoint()`, none of which exist in the `WP05` implementation (which uses different method names like `load_state`, `update_status`, `save_candidate` etc.).
3. **Enum Conflict**: `orchestrator.py` expects `ExperimentState` from `src.runner.state`, but `WP05` defines `ExperimentStatus`.
4. **Branching Issue**: WP06 appears to have been branched from `main` without incorporating the changes from the dependency WP05.

**Action Required**:

- Rebase WP06 on the completed WP05 implementation.
- Align `orchestrator.py` with the actual API of `ExperimentStateManager` and `Executors` implemented in WP05.
- Ensure all necessary files are present in the branch.


## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T12:02:11Z – Antigravity – shell_pid=922104 – lane=doing – Assigned agent via workflow command
- 2026-02-27T12:07:58Z – Antigravity – shell_pid=922104 – lane=for_review – Ready for review
- 2026-02-27T12:16:27Z – Antigravity – shell_pid=922104 – lane=doing – Started review via workflow command
- 2026-02-27T12:19:02Z – Antigravity – shell_pid=922104 – lane=planned – Moved to planned
- 2026-02-27T12:25:40Z – Antigravity – shell_pid=922104 – lane=doing – Started implementation via workflow command

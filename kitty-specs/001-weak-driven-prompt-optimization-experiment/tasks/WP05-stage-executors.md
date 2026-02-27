---
work_package_id: WP05
title: Experiment Stage Executors
lane: "doing"
dependencies: [WP02, WP03, WP04]
base_branch: main
base_commit: 535043111edae4ee24837510cf9c71ee3206b747
created_at: '2026-02-27T11:28:11.955287+00:00'
subtasks: [T013, T014, T015]
requirement_refs: [FR-004]
shell_pid: "922104"
agent: "Antigravity"
---

# Work Package Prompt: WP05 - Experiment Stage Executors

## Context & Objective
Isolate the complex business logic of the individual experimental stages into dedicated Executor classes. This prevents the main runner from becoming a monolithic, hard-to-maintain file and clearly delineates the boundaries of Large Model baseline vs Small Model hardening vs Final Evaluation.

## Subtasks & Detailed Guidance

### Subtask T013: Implement `Stage1Executor` (Baseline Large Model)
- **Purpose**: Encapsulate the logic for optimizing the initial prompt on the large frontier model.
- **Steps**:
  1. Create `src/runner/executors.py`.
  2. Create `Stage1Executor`. It should accept the DSPy optimizer (WP03), Data loader (WP02), and State Manager (WP04).
  3. Execute the baseline optimization loop, decrementing the budget in the state manager.
  4. Return and checkpoint the optimized `PromptCandidate`.
- **Files**: `src/runner/executors.py`

### Subtask T014: Implement `Stage2Executor` (Hardening Small Model)
- **Purpose**: Encapsulate the core novelty logic: forcing the prompt to evolve against the small model's failures.
- **Steps**:
  1. Create `Stage2Executor`.
  2. It accepts the baseline `PromptCandidate` from Stage 1.
  3. Switch the DSPy execution context to evaluate using the weak/small model.
  4. Run the GEPA optimizer loop until the budget is exhausted or convergence occurs.
  5. Return and checkpoint the hardened `PromptCandidate`.
- **Files**: `src/runner/executors.py`

### Subtask T015: Implement `Stage3Executor` (Re-evaluation)
- **Purpose**: Standardize the final evaluation phase for both baseline and hardened prompts.
- **Steps**:
  1. Create `Stage3Executor`.
  2. Accept a `PromptCandidate` and standard benchmark datasets.
  3. Execute the evaluation harness (without optimization).
  4. Save `ModelOutputRecord`s via `DatasetExporter` and return the final `EvaluationResult`.
- **Files**: `src/runner/executors.py`

## Risks & Review Guidance
- **Context Bleed**: Ensure that Stage 2 correctly routes the *evaluator* role to the small model while still allowing the *optimizer* (the one proposing prompt changes) to remain the large model if dictated by GEPA, or correctly configured as per the research design.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T11:28:12Z – Antigravity – shell_pid=922104 – lane=doing – Assigned agent via workflow command

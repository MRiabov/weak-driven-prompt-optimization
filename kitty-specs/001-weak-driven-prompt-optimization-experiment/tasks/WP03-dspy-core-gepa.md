---
work_package_id: WP03
title: DSPy Core and GEPA Integration
lane: "for_review"
dependencies: [WP01]
base_branch: main
base_commit: 940e868c65de5a320ede4fe0d7de51f5f9ca8c9f
created_at: '2026-02-27T10:50:29.825535+00:00'
subtasks: [T007, T008, T009]
agent: Gemini-CLI
shell_pid: '903358'
requirement_refs: [FR-001, FR-006]
---

# Work Package Prompt: WP03 - DSPy Core and GEPA Integration

## Context & Objective
This work package implements the core optimization engine. You will define the DSPy programs (signatures and modules) that process the benchmarks, and construct the optimization loop (incorporating GEPA concepts) for both the baseline (Stage 1) and weak-agent hardening (Stage 2).

## Subtasks & Detailed Guidance

### Subtask T007: Implement DSPy signatures and modules
- **Purpose**: Define the prompt structures and the execution logic for the LLM.
- **Steps**:
  1. Create `src/optimization/modules.py`.
  2. Define a `dspy.Signature` for solving the benchmark problems (e.g., `Question -> Answer`).
  3. Define a `dspy.Module` (e.g., a Predict or ChainOfThought module) that utilizes the signature.
- **Files**: `src/optimization/modules.py`
- **Parallel?**: Yes, independent of WP02.

### Subtask T008: Integrate GEPA optimizer for the baseline stage
- **Purpose**: Implement the Stage 1 optimization loop using a large model.
- **Steps**:
  1. Create `src/optimization/optimizer.py`.
  2. Configure a DSPy optimizer (e.g., `MIPROv2`, `COPRO`, or a custom teleprompter implementing GEPA logic) to optimize the instructions of the module defined in T007.
  3. The optimizer must use the large model (e.g., Trinity-Large-Preview).
  4. The function should return the optimized `PromptCandidate`.
- **Files**: `src/optimization/optimizer.py`

### Subtask T009: Implement weak-agent hardening stage logic
- **Purpose**: Implement the Stage 2 optimization loop where the baseline prompt is evolved against the failures of a small model.
- **Steps**:
  1. In `src/optimization/optimizer.py`, add the hardening logic.
  2. Initialize the optimization loop using the baseline prompt candidate as the starting point.
  3. Configure the optimizer to use the small model (e.g., Step-3.5-Flash) for evaluation, forcing the optimizer to rewrite the prompt to account for the weak model's errors.
  4. Return the new hardened `PromptCandidate`.

## Risks & Review Guidance
- **DSPy complexity**: DSPy optimizers can be complex to configure. Ensure the chosen optimizer closely mimics the GEPA approach (reflective evolution) described in the research plan.
- **Model routing**: Ensure the large model is used as the *optimizer* (the one proposing changes) while the small model is used as the *evaluator* (the one attempting the task) during Stage 2.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
- 2026-02-27T10:50:29Z – Gemini-CLI – shell_pid=903358 – lane=doing – Assigned agent via workflow command
- 2026-02-27T10:54:46Z – Gemini-CLI – shell_pid=903358 – lane=for_review – Implemented DSPy modules and GEPA optimizer for Stage 1 (Strong-to-Strong) and Stage 2 (Strong-to-Weak) optimization. Added integration tests.

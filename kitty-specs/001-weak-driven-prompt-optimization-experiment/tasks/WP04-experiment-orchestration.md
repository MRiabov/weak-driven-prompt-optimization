---
work_package_id: "WP04"
title: "Experiment Orchestration Pipeline"
lane: "planned"
requirement_refs: ["FR-004", "FR-005", "FR-006"]
dependencies: ["WP02", "WP03"]
subtasks: ["T010", "T011", "T012"]
---

# Work Package Prompt: WP04 - Experiment Orchestration Pipeline

## Context & Objective
The orchestration pipeline represents the core logic loop of the research application. It connects the data loaders, DSPy optimizers, and evaluations. This work package focuses on the backend implementation of this pipeline and how state is tracked, avoiding mixing it with the CLI interface which will come later.

## Subtasks & Detailed Guidance

### Subtask T010: Implement `ExperimentRunner` and stage management logic
- **Purpose**: Build the class responsible for executing arbitrary experimental stages.
- **Steps**:
  1. Create `src/runner.py`.
  2. Implement an `ExperimentRunner` class.
  3. Add methods for abstracting stage runs (e.g., setting up the data iterators from WP02, passing them to the optimizers from WP03, and collecting the results).
- **Files**: `src/runner.py`

### Subtask T011: Wire up the Stage 1 -> Stage 2 -> Stage 3 transitions
- **Purpose**: Implement the specific business logic for the Large-Small-Large pipeline.
- **Steps**:
  1. Implement `run_full_experiment(self, config: ExperimentConfig)`.
  2. **Stage 1**: Call the baseline optimizer on the large model, capturing the resulting `PromptCandidate`.
  3. **Stage 2**: Pass the Stage 1 `PromptCandidate` to the weak-agent hardening logic using the small model, returning the final hardened `PromptCandidate`.
  4. **Stage 3**: Perform an evaluation run using the *large model* but supplying the *hardened prompt* from Stage 2. Capture the `EvaluationResult`.
  5. For comparative purposes, also run an evaluation of the Stage 1 prompt on the large model (the baseline performance).
  6. Return the consolidated results.

### Subtask T012: Implement intermediate state persistence for resumption
- **Purpose**: Ensure long-running optimization jobs don't lose progress on failure.
- **Steps**:
  1. Create `src/state_manager.py` or integrate directly into the runner.
  2. Implement logic that saves the `PromptCandidate` JSON representations to disk at the end of Stage 1 and Stage 2.
  3. Implement logic that checks if a Stage 1 file exists before starting; if it does, prompt or automatically resume directly from Stage 2.
  4. Ensure `EvaluationResult` objects are also saved in a persistent registry (JSON or sqlite) so the CLI can query them later.

## Risks & Review Guidance
- **State Management**: Handling intermediate states correctly is crucial for cost savings and developer experience during testing. Ensure the files are clearly identifiable by the `experiment_id`.
- **Memory/Disk I/O**: Ensure the runner isn't holding thousands of outputs in memory. It should pass data directly to the `DatasetExporter` implemented in WP02.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
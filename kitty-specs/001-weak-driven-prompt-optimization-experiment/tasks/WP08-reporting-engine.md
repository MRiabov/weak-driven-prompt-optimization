---
work_package_id: WP08
title: Reporting Engine
lane: "doing"
dependencies: [WP06]
base_branch: main
base_commit: c86dc770ac0e1326be5fdf0c2a884db71992a433
created_at: '2026-02-27T14:01:39.270721+00:00'
subtasks: [T020, T021, T022]
requirement_refs: [FR-005]
shell_pid: "922104"
---

# Work Package Prompt: WP08 - Reporting Engine

## Context & Objective
The entire purpose of this feature is research. The reporting engine is responsible for digesting the output of Stage 3 and presenting an analytical comparison that answers the research question: "Did the weak-hardened prompt perform better?"

## Subtasks & Detailed Guidance

### Subtask T020: Implement data aggregation logic
- **Purpose**: Load and compare evaluation results.
- **Steps**:
  1. Create `src/reporting/analyzer.py`.
  2. Implement logic that takes an `experiment_id`, loads the `EvaluationResult` objects from disk for both the baseline and hardened prompts.
  3. Calculate relative differences (e.g., +5% accuracy, -10% cost).
- **Files**: `src/reporting/analyzer.py`

### Subtask T021: Implement markdown report generator
- **Purpose**: Format the findings clearly.
- **Steps**:
  1. Create a function that templates the aggregated data into a clean Markdown format.
  2. Include sections for: Configuration used, Baseline Performance, Hardened Performance, Cost/Duration comparison, and a conclusion summary.
- **Files**: `src/reporting/analyzer.py`

### Subtask T022: Add `report` command to CLI
- **Purpose**: Allow users to generate reports on demand.
- **Steps**:
  1. In `main.py`, add a `report` subcommand.
  2. Accept `--experiment-id`.
  3. Call the analyzer and output the markdown to `stdout` or an `--output` file.
- **Files**: `main.py`

## Risks & Review Guidance
- **Metrics Accuracy**: Ensure the delta calculations are mathematically sound and correctly label the large vs small models to avoid misleading conclusions in the research paper.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.

---
work_package_id: "WP05"
title: "CLI Application and Reporting"
lane: "planned"
requirement_refs: ["FR-003"]
dependencies: ["WP04"]
subtasks: ["T013", "T014", "T015"]
---

# Work Package Prompt: WP05 - CLI Application and Reporting

## Context & Objective
Provide a clean user interface to interact with the experiment runner. This work package wraps the logic implemented in WP04 in a terminal application, enabling users to pass configurations via YAML files and output comparative analytical reports.

## Subtasks & Detailed Guidance

### Subtask T013: Build the CLI entrypoint with configuration parsing
- **Purpose**: Create the main executable entrypoint for the user.
- **Steps**:
  1. Create `main.py` at the root of the project.
  2. Integrate `argparse` or `click` to handle command-line arguments.
  3. Implement a configuration loader that reads a YAML file and converts it into the `ExperimentConfig` Pydantic model (from WP01).
- **Files**: `main.py`

### Subtask T014: Implement the `run-experiment` command
- **Purpose**: Trigger the `ExperimentRunner` from the terminal.
- **Steps**:
  1. Add a command `run-experiment` taking a `--config` argument.
  2. Instantiate `ExperimentRunner` (WP04) and pass the configuration.
  3. Ensure console output (logging) gives the user real-time feedback on what stage the pipeline is currently in.

### Subtask T015: Implement the analytical report generator
- **Purpose**: Compare the baseline and hardened prompts to prove or disprove the hypothesis.
- **Steps**:
  1. Add a `report` command to the CLI taking an `--experiment-id` argument.
  2. The logic should read the saved `EvaluationResult` files corresponding to that experiment ID.
  3. It must extract the accuracy/metrics for:
     - Baseline Prompt on Large Model
     - Hardened Prompt on Large Model
  4. Print a markdown-formatted or tabular summary to stdout. It should highlight the absolute and relative difference in performance, API costs, and total duration.

## Risks & Review Guidance
- **User Experience**: The CLI should fail fast if the configuration is invalid or missing environment variables before starting expensive external processes.
- **Reporting Metrics**: Ensure the comparison logic strictly compares apples to apples (same model, same benchmark, different prompts).

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
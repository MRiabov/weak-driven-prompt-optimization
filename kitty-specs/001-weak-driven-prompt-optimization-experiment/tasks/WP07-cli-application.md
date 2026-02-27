---
work_package_id: "WP07"
title: "CLI Application"
lane: "planned"
requirement_refs: ["FR-003"]
dependencies: ["WP06"]
subtasks: ["T018", "T019"]
---

# Work Package Prompt: WP07 - CLI Application

## Context & Objective
Provide the user interface to trigger the experiment runner. This focuses purely on argument parsing, reading the configuration YAML, and executing the orchestrator.

## Subtasks & Detailed Guidance

### Subtask T018: Build CLI entrypoint (`main.py`)
- **Purpose**: Create the main executable interface.
- **Steps**:
  1. Create `main.py` at the project root.
  2. Use `argparse` or `click` to implement a base CLI group.
  3. Implement logging configuration to output runner progress to `stdout`.
- **Files**: `main.py`

### Subtask T019: Implement `run-experiment` command
- **Purpose**: Execute the orchestration pipeline.
- **Steps**:
  1. Add a `run-experiment` subcommand.
  2. Accept a `--config` argument pointing to a YAML file.
  3. Parse the YAML into the `ExperimentConfig` Pydantic model.
  4. Instantiate `ExperimentRunner` and call `run()`.
- **Files**: `main.py`

## Risks & Review Guidance
- **Configuration Validation**: The CLI must catch malformed YAML files or missing required fields immediately and provide a helpful error message before starting the runner.

## Activity Log
- 2026-02-27T00:00:00Z – system – lane=planned – Prompt created.
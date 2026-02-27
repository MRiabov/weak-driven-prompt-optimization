---
work_package_id: WP07
title: CLI Application
lane: "done"
dependencies: [WP06]
base_branch: main
base_commit: 898de941d75196cf5fe08b0adcea05df3c75c267
created_at: '2026-02-27T12:39:32.420973+00:00'
subtasks: [T018, T019]
agent: Antigravity
shell_pid: '922104'
requirement_refs: [FR-003]
reviewed_by: "MRiabov"
review_status: "approved"
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
- 2026-02-27T12:39:32Z – Antigravity – shell_pid=978047 – lane=doing – Assigned agent via workflow command
- 2026-02-27T12:43:39Z – Antigravity – shell_pid=978047 – lane=for_review – Ready for review: Implemented main.py with run-experiment command and YAML parsing
- 2026-02-27T12:45:48Z – Antigravity – shell_pid=922104 – lane=doing – Started review via workflow command
- 2026-02-27T12:52:37Z – Antigravity – shell_pid=922104 – lane=done – Review passed: Successfully implemented CLI with run-experiment command parsing YAML into ExperimentConfig and running ExperimentRunner. Error handling verified against malformed configs. Also verified passing tests.

# Work Packages

## Context
**Feature**: 001-weak-driven-prompt-optimization-experiment
**Branch**: 001-weak-driven-prompt-optimization-experiment
**Target completion**: Phase 1

## Work Packages

### Setup & Foundation

### WP01: Foundation and Models
**Summary**: Set up the Python environment, dependencies, and define the core Pydantic data models.
**Requirement Refs**: FR-001, FR-003
**Included Subtasks**:
- [x] T001: Set up project environment (pyproject.toml/requirements.txt)
- [x] T002: Implement Pydantic domain models
- [x] T003: Configure Langfuse tracing and OpenRouter clients
**Implementation Notes**: Must ensure strict schema validation using Pydantic as per the constitution.
**Parallel Opportunities**: None
**Dependencies**: None
**Prompt File**: WP01-foundation-and-models.md

### Core Evaluation & Data

### WP02: Data Loading and Evaluation Harness
**Summary**: Implement streaming data loaders for HuggingFace datasets and define the evaluation metrics.
**Requirement Refs**: FR-002, FR-005
**Included Subtasks**:
- [x] T004: Implement HuggingFace dataset streaming loaders
- [x] T005: Implement metric evaluation functions
- [x] T006: Implement `DatasetExporter` for JSONL output
**Implementation Notes**: Streaming must be used for datasets to avoid large local downloads.
**Parallel Opportunities**: Yes, independent of WP03.
**Dependencies**: WP01
**Prompt File**: WP02-data-loading-and-evaluation.md

### Optimization Pipeline

### WP03: DSPy Core and GEPA Integration
**Summary**: Build the DSPy signatures, modules, and the GEPA optimization logic for both the baseline and weak-agent stages.
**Requirement Refs**: FR-001, FR-006
**Included Subtasks**:
- [x] T007: Implement DSPy signatures and modules
- [x] T008: Integrate GEPA optimizer for the baseline stage
- [x] T009: Implement weak-agent hardening stage logic
**Implementation Notes**: Langfuse tracing must wrap the DSPy executions.
**Parallel Opportunities**: Yes, independent of WP02.
**Dependencies**: WP01
**Prompt File**: WP03-dspy-core-gepa.md

### Orchestration & State Management

### WP04: State Management and Checkpointing
**Summary**: Build a robust state manager to persist progress, handle budget constraints, and enable run resumption.
**Requirement Refs**: FR-005, FR-006
**Included Subtasks**:
- [x] T010: Implement `ExperimentState` manager
- [x] T011: Implement budget iteration tracking
- [x] T012: Implement save/load checkpoints for models
**Implementation Notes**: Essential for cost-savings. If the script crashes, we shouldn't lose expensive OpenRouter API outputs.
**Parallel Opportunities**: None
**Dependencies**: WP01
**Prompt File**: WP04-state-management.md

### WP05: Experiment Stage Executors
**Summary**: Isolate the business logic for each experimental stage into dedicated executor classes.
**Requirement Refs**: FR-004
**Included Subtasks**:
- [ ] T013: Implement `Stage1Executor` (Baseline Large Model)
- [ ] T014: Implement `Stage2Executor` (Hardening Small Model)
- [ ] T015: Implement `Stage3Executor` (Re-evaluation)
**Implementation Notes**: These classes should wrap the DSPy optimization loops with logging and state updates.
**Parallel Opportunities**: None
**Dependencies**: WP02, WP03, WP04
**Prompt File**: WP05-stage-executors.md

### WP06: Pipeline Orchestrator
**Summary**: The main loop that connects the stages and manages the overall workflow.
**Requirement Refs**: FR-004
**Included Subtasks**:
- [ ] T016: Implement the `ExperimentRunner`
- [ ] T017: Wire transitions (Stage 1 -> Stage 2 -> Stage 3)
**Implementation Notes**: Passes outputs of one stage as inputs to the next.
**Parallel Opportunities**: None
**Dependencies**: WP05
**Prompt File**: WP06-pipeline-orchestrator.md

### Reporting & Interaction

### WP07: CLI Application
**Summary**: Provide the user interface to trigger the experiment runner.
**Requirement Refs**: FR-003
**Included Subtasks**:
- [ ] T018: Build CLI entrypoint (`main.py`)
- [ ] T019: Implement `run-experiment` command
**Implementation Notes**: Use standard libraries like argparse or click.
**Parallel Opportunities**: None
**Dependencies**: WP06
**Prompt File**: WP07-cli-application.md

### WP08: Reporting Engine
**Summary**: Aggregate data and generate analytical comparison reports.
**Requirement Refs**: FR-005
**Included Subtasks**:
- [ ] T020: Implement data aggregation logic
- [ ] T021: Implement markdown report generator
- [ ] T022: Add `report` command to CLI
**Implementation Notes**: Compare baseline vs hardened prompt accuracy.
**Parallel Opportunities**: Yes, parallel with WP07.
**Dependencies**: WP06
**Prompt File**: WP08-reporting-engine.md

### Validation

### WP09: Integration Testing
**Summary**: Validate the entire end-to-end system using mock LLMs as mandated by the constitution.
**Requirement Refs**: FR-004
**Included Subtasks**:
- [ ] T023: Implement mock LLM client for DSPy
- [ ] T024: Write end-to-end integration tests
**Implementation Notes**: No unit tests. Only black-box testing of the full workflow.
**Parallel Opportunities**: None
**Dependencies**: WP07, WP08
**Prompt File**: WP09-integration-testing.md

<!-- status-model:start -->
## Canonical Status (Generated)
- WP01: done
- WP02: done
- WP03: done
<!-- status-model:end -->

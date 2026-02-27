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
**Priority**: P0 (Blocker for all other work)
**Independent Test**: Can instantiate models and validate mock configurations.
**Included Subtasks**:
- [ ] T001: Set up project environment (pyproject.toml/requirements.txt)
- [ ] T002: Implement Pydantic domain models
- [ ] T003: Configure Langfuse tracing and OpenRouter clients
**Implementation Notes**: Must ensure strict schema validation using Pydantic as per the constitution.
**Parallel Opportunities**: None
**Dependencies**: None
**Prompt File**: WP01-foundation-and-models.md

### Core Evaluation & Data

### WP02: Data Loading and Evaluation Harness
**Summary**: Implement streaming data loaders for HuggingFace datasets and define the evaluation metrics.
**Requirement Refs**: FR-002, FR-005
**Priority**: P1
**Independent Test**: Can stream records from HF datasets and execute metric evaluation functions.
**Included Subtasks**:
- [ ] T004: Implement HuggingFace dataset streaming loaders
- [ ] T005: Implement metric evaluation functions
- [ ] T006: Implement `DatasetExporter` for JSONL output
**Implementation Notes**: Streaming must be used for datasets to avoid large local downloads.
**Parallel Opportunities**: Yes, independent of WP03.
**Dependencies**: WP01
**Prompt File**: WP02-data-loading-and-evaluation.md

### Optimization Pipeline

### WP03: DSPy Core and GEPA Integration
**Summary**: Build the DSPy signatures, modules, and the GEPA optimization logic for both the baseline and weak-agent stages.
**Requirement Refs**: FR-001, FR-006
**Priority**: P1
**Independent Test**: Can run a mock DSPy optimization loop returning a modified prompt.
**Included Subtasks**:
- [ ] T007: Implement DSPy signatures and modules
- [ ] T008: Integrate GEPA optimizer for the baseline stage
- [ ] T009: Implement weak-agent hardening stage logic
**Implementation Notes**: Langfuse tracing must wrap the DSPy executions.
**Parallel Opportunities**: Yes, independent of WP02.
**Dependencies**: WP01
**Prompt File**: WP03-dspy-core-gepa.md

### Orchestration

### WP04: Experiment Orchestration Pipeline
**Summary**: Tie the stages together into a unified pipeline (Baseline -> Hardening -> Eval) including state persistence.
**Requirement Refs**: FR-004, FR-005, FR-006
**Priority**: P1
**Independent Test**: The orchestrator can run the three stages and save state correctly using mock models.
**Included Subtasks**:
- [ ] T010: Implement `ExperimentRunner` and stage management logic
- [ ] T011: Wire up the Stage 1 -> Stage 2 -> Stage 3 transitions
- [ ] T012: Implement intermediate state persistence for resumption
**Implementation Notes**: Ensure intermediate prompt candidates and evaluation results are saved dynamically so crashes don't wipe progress.
**Parallel Opportunities**: None
**Dependencies**: WP02, WP03
**Prompt File**: WP04-experiment-orchestration.md

### Reporting & Interaction

### WP05: CLI Application and Reporting
**Summary**: Provide the user interface to run the experiment and generate comparative reports.
**Requirement Refs**: FR-003
**Priority**: P1
**Independent Test**: Can invoke the CLI with a config file and trigger the pipeline, and view a report.
**Included Subtasks**:
- [ ] T013: Build the CLI entrypoint with configuration parsing
- [ ] T014: Implement the `run-experiment` command
- [ ] T015: Implement the analytical report generator
**Implementation Notes**: Use standard libraries like argparse or click. The report should output directly to console or markdown.
**Parallel Opportunities**: Report logic (T015) can be built in parallel with CLI entrypoint (T013).
**Dependencies**: WP04
**Prompt File**: WP05-cli-and-reporting.md

### Validation

### WP06: Integration Testing
**Summary**: Validate the entire end-to-end system using mock LLMs as mandated by the constitution.
**Requirement Refs**: FR-004
**Priority**: P2
**Independent Test**: The test suite runs and passes.
**Included Subtasks**:
- [ ] T016: Implement mock LLM client for DSPy
- [ ] T017: Write end-to-end integration tests
**Implementation Notes**: No unit tests. Only black-box testing of the full workflow.
**Parallel Opportunities**: None
**Dependencies**: WP05
**Prompt File**: WP06-integration-testing.md
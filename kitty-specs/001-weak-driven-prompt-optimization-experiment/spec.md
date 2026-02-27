# Feature Specification: Weak-Driven Prompt Optimization Experiment

**Feature Branch**: `001-weak-driven-prompt-optimization-experiment`
**Created**: 2026-02-27
**Status**: Draft
**Input**: User description: "Help me specify the research task as per @idea.md and, more verbosely, @Gemini-Prompt Optimization Research Plan.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Baseline Large Model Performance Optimization (Priority: P1)

As an AI researcher, I want to establish a baseline performance metric by optimizing a prompt exclusively on the large frontier model, so I can compare it against the multi-model approach.

**Why this priority**: Without a baseline, we cannot measure the impact of the proposed Large-Small-Large optimization framework. It establishes the "control group" for the experiment.

**Independent Test**: Can be fully tested by running the prompt optimization process on the designated large model (`arcee-ai/trinity-large-preview:free`) using the specified benchmarks, and measuring its final accuracy.

**Acceptance Scenarios**:

1. **Given** a set of initial, unoptimized prompts for the chosen benchmarks, **When** the system runs the optimization cycle solely using the large model, **Then** a final optimized prompt and a baseline accuracy score are produced for each benchmark.
2. **Given** a budget constraint on optimization iterations, **When** the baseline optimization is executed, **Then** it halts when the iteration limit or convergence threshold is reached.

---

### User Story 2 - Weak-Agent Prompt Hardening (Priority: P1)

As an AI researcher, I want to take the baseline-optimized prompt and further evolve it using a smaller, weak model, so that the weak model's failures force the discovery of more robust, edge-case-resistant instructions.

**Why this priority**: This is the core novelty of the experiment. Evolving the prompt against the weak model is the mechanism hypothesized to overcome prompt saturation.

**Independent Test**: Can be tested by taking the output of User Story 1, applying the optimization cycle on the weak model (`stepfun/step-3.5-flash:free`), and verifying that the resulting prompt changes structurally to become more explicit or procedural.

**Acceptance Scenarios**:

1. **Given** the baseline optimized prompt, **When** it is subjected to optimization using only the weak model's evaluation, **Then** a new, "hardened" prompt is produced.
2. **Given** the optimization process on the weak model, **When** the weak model fails on a test case, **Then** the system proposes prompt mutations specifically designed to address that failure mode.

---

### User Story 3 - Frontier Model Re-evaluation and Comparison (Priority: P1)

As an AI researcher, I want to deploy the weak-hardened prompt back to the original large model and compare its performance against the baseline, so I can validate whether the weak-driven learning actually improved the large model's capabilities.

**Why this priority**: This is the final validation step that proves or disproves the core hypothesis of the research experiment.

**Independent Test**: Can be tested by running the original benchmark suite on the large model using the newly "hardened" prompt and statistically comparing the results to the baseline score from User Story 1.

**Acceptance Scenarios**:

1. **Given** the hardened prompt from the weak model and the baseline prompt, **When** both are evaluated on the large model against the full benchmark suites, **Then** a comparative performance report is generated.
2. **Given** the performance report, **When** the hardened prompt scores higher than the baseline prompt, **Then** the system highlights the specific test cases where the hardened prompt succeeded and the baseline failed.

---

### Edge Cases

- What happens if the weak model fails 100% of the time on a specific benchmark, providing no "success" signal for the optimizer to learn from?
- How does the system handle API rate limits or failures when querying the external model providers (OpenRouter) during a long optimization run?
- What happens if the hardened prompt becomes so long or complex that it exceeds the context window limits of either the large or small model?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support execution of optimization pipelines using designated large and small LLMs via an external API (OpenRouter).
- **FR-002**: The system MUST implement an evaluation harness for the FRONTIERMATH, SuperGPQA, and tau^2-Bench benchmarks.
- **FR-003**: The system MUST allow configuring the specific models to use via environment variables or a configuration file.
- **FR-004**: The system MUST execute a three-stage optimization pipeline: (1) Large model baseline optimization, (2) Small model prompt hardening, (3) Large model final evaluation.
- **FR-005**: The system MUST record and persist the prompt states, evaluation scores, and iteration counts at the end of each stage.
- **FR-006**: The system MUST ensure that the total optimization budget (e.g., total number of iterations) is tracked and can be constrained to allow for a "budget-equivalent" comparison between the baseline and the LSL framework.

### Key Entities

- **Experiment Run**: Represents a full execution of the LSL framework. Contains the configuration (models, benchmarks, budget), intermediate prompts, and final evaluation results.
- **Prompt Candidate**: A specific iteration of a prompt string, associated with the model it was optimized for and its score on a given benchmark.
- **Evaluation Result**: The performance metric (accuracy, success rate) achieved by a specific Prompt Candidate on a specific Benchmark Dataset using a specific LLM.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The experimental pipeline completes all three stages (Large -> Small -> Large) automatically without manual intervention for all specified benchmarks.
- **SC-002**: The system generates a final analytical report that explicitly compares the performance (accuracy/success rate) of the Baseline Prompt vs. the Hardened Prompt on the large model.
- **SC-003**: The system records the API costs and time duration for the entire experiment, enabling an efficiency comparison against alternative optimization methods.
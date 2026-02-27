# Research: Weak-Driven Prompt Optimization

## Decision: HuggingFace Datasets via Streaming
- **Rationale**: The specification requires testing on FRONTIERMATH, SuperGPQA, and tau^2-Bench. These can be large. Streaming allows us to evaluate without massive local downloads.
- **Alternatives considered**: Downloading JSONL files manually. Rejected due to manual overhead and storage requirements.

## Decision: DSPy with custom GEPA integration
- **Rationale**: DSPy provides native optimization abstractions, prompt signatures, and metric evaluation. We will integrate GEPA logic into DSPy's teleprompter/optimizer loops to enable the Large-Small-Large cycle.
- **Alternatives considered**: Building a custom prompt optimization loop from scratch. Rejected because DSPy already handles the heavy lifting of prompting and tracing.

## Decision: Langfuse for Observability
- **Rationale**: Langfuse integrates well with DSPy and provides excellent tracing, cost tracking, and versioning for prompt optimization. It fulfills the requirement to track API costs and iterations efficiently.
- **Alternatives considered**: Weights & Biases (wandb). Langfuse is more specialized for LLM tracing and prompt versioning.

## Decision: OpenRouter via OpenAI Client
- **Rationale**: OpenRouter provides access to both `arcee-ai/trinity-large-preview:free` (large) and `stepfun/step-3.5-flash:free` (small). DSPy supports OpenAI-compatible endpoints natively.
- **Alternatives considered**: Direct API integrations for each provider. Rejected due to complexity; OpenRouter provides a unified interface.

## Decision: Model Output Persistence via JSONL
- **Rationale**: Persisting the raw model outputs alongside the evaluations enables deeper offline analysis of failure modes and edge cases discovered by the weak model without having to re-run expensive LLM inference.
- **Alternatives considered**: Saving exclusively to Langfuse. Rejected because offline, bulk analytical queries over specific generations are much easier with flat JSONL/HF Datasets directly tied to the experiment ID.
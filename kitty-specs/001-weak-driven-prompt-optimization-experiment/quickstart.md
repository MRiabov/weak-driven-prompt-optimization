# Quickstart

## Setup

1. Clone the repository and navigate to the project root.
2. Ensure Python 3.12 is installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   export OPENROUTER_API_KEY="your_openrouter_api_key"
   export LANGFUSE_PUBLIC_KEY="your_langfuse_public"
   export LANGFUSE_SECRET_KEY="your_langfuse_secret"
   export LANGFUSE_HOST="https://cloud.langfuse.com"
   ```

## Running the Experiment

To run the full LSL pipeline:

```bash
python main.py run-experiment --config config.yaml
```

To view results:

```bash
python main.py report --experiment-id <id>
```
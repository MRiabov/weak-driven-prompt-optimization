import os
import dspy
from langfuse import Langfuse
from dspy.utils.callback import BaseCallback

class LangfuseCallback(BaseCallback):
    """
    Custom Langfuse callback for DSPy.
    """
    def __init__(self, public_key, secret_key, host):
        self.langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host
        )
        self.active_generations = {}

    def on_lm_start(self, call_id, instance, inputs):
        # Create a generation in Langfuse
        generation = self.langfuse.generation(
            name=f"dspy_lm_{instance.model if hasattr(instance, 'model') else 'unknown'}",
            input=inputs,
            model=getattr(instance, "model", None)
        )
        self.active_generations[call_id] = generation

    def on_lm_end(self, call_id, outputs, exception=None):
        generation = self.active_generations.pop(call_id, None)
        if generation:
            if exception:
                generation.update(output=str(exception), level="ERROR")
            else:
                generation.update(output=outputs)

def init_langfuse():
    """
    Initialize Langfuse client and return the callback handler for DSPy.
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        raise ValueError("LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY must be set in environment variables.")

    handler = LangfuseCallback(
        public_key=public_key,
        secret_key=secret_key,
        host=host
    )
    
    return handler

def setup_dspy_tracing(handler: LangfuseCallback):
    """
    Configure DSPy to use the Langfuse callback handler.
    """
    dspy.settings.configure(callbacks=[handler])

import os
import dspy

def get_llm_client(model_name: str, **kwargs):
    """
    Returns a DSPy LM client configured for OpenRouter.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY must be set in environment variables.")

    # OpenRouter is OpenAI-compatible
    lm = dspy.LM(
        model=model_name,
        api_base="https://openrouter.ai/api/v1",
        api_key=api_key,
        **kwargs
    )
    
    return lm

def configure_dspy_lm(lm: dspy.LM):
    """
    Set the default LM for DSPy.
    """
    dspy.settings.configure(lm=lm)

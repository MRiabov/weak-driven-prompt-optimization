import pytest
import os
from src.utils.observability import init_langfuse, LangfuseCallback
from src.utils.llm_client import get_llm_client

def test_init_langfuse_no_keys():
    if "LANGFUSE_PUBLIC_KEY" in os.environ:
        del os.environ["LANGFUSE_PUBLIC_KEY"]
    if "LANGFUSE_SECRET_KEY" in os.environ:
        del os.environ["LANGFUSE_SECRET_KEY"]
    
    with pytest.raises(ValueError, match="LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY must be set"):
        init_langfuse()

def test_init_langfuse_success(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    
    handler = init_langfuse()
    assert isinstance(handler, LangfuseCallback)

def test_get_llm_client_no_key():
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]
    
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY must be set"):
        get_llm_client(model_name="test-model")

import pytest
from unittest.mock import MagicMock, patch
import dspy
from src.optimization.modules import QAModule, QASignature
from src.optimization.optimizer import optimize_baseline, harden_prompt, extract_prompt_from_module
from src.models.domain import PromptCandidate, PromptStage

def test_qa_module():
    module = QAModule()
    assert isinstance(module, dspy.Module)
    assert hasattr(module, "generate_answer")
    # In DSPy, ChainOfThought wraps the signature and adds reasoning
    # We check if the instructions match or if it contains the fields
    signature = module.generate_answer.predict.signature
    assert "question" in signature.input_fields
    assert "answer" in signature.output_fields

def test_extract_prompt_from_module():
    module = QAModule()
    # Mock signature instructions
    for name, parameter in module.named_predictors():
        parameter.signature.instructions = "Test instructions"
    
    prompt = extract_prompt_from_module(module)
    assert prompt == "Test instructions"

@patch("src.optimization.optimizer.get_llm_client")
@patch("src.optimization.optimizer.GEPA")
def test_optimize_baseline(mock_gepa_class, mock_get_llm):
    # Setup mocks
    mock_lm = MagicMock()
    mock_get_llm.return_value = mock_lm
    
    mock_optimizer = MagicMock()
    mock_gepa_class.return_value = mock_optimizer
    
    # Mock compiled module
    mock_compiled_module = QAModule()
    for name, parameter in mock_compiled_module.named_predictors():
        parameter.signature.instructions = "Optimized instructions"
    mock_optimizer.compile.return_value = mock_compiled_module
    
    trainset = [dspy.Example(question="2+2", answer="4").with_inputs("question")]
    
    candidate = optimize_baseline(trainset, "strong-model")
    
    assert isinstance(candidate, PromptCandidate)
    assert candidate.stage == PromptStage.BASELINE
    assert candidate.content == "Optimized instructions"
    mock_optimizer.compile.assert_called_once()

@patch("src.optimization.optimizer.get_llm_client")
@patch("src.optimization.optimizer.GEPA")
def test_harden_prompt(mock_gepa_class, mock_get_llm):
    # Setup mocks
    mock_lm = MagicMock()
    mock_get_llm.return_value = mock_lm
    
    mock_optimizer = MagicMock()
    mock_gepa_class.return_value = mock_optimizer
    
    # Mock compiled module
    mock_compiled_module = QAModule()
    for name, parameter in mock_compiled_module.named_predictors():
        parameter.signature.instructions = "Hardened instructions"
    mock_optimizer.compile.return_value = mock_compiled_module
    
    trainset = [dspy.Example(question="3+3", answer="6").with_inputs("question")]
    baseline_candidate = PromptCandidate(
        prompt_id="p1",
        stage=PromptStage.BASELINE,
        content="Baseline instructions"
    )
    
    candidate = harden_prompt(trainset, baseline_candidate, "strong-model", "weak-model")
    
    assert isinstance(candidate, PromptCandidate)
    assert candidate.stage == PromptStage.HARDENED
    assert candidate.content == "Hardened instructions"
    assert candidate.parent_prompt_id == "p1"
    mock_optimizer.compile.assert_called_once()

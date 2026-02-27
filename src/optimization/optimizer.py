import uuid
import dspy
from dspy.teleprompt import GEPA
from src.utils.llm_client import get_llm_client, configure_dspy_lm
from src.optimization.modules import QAModule
from src.models.domain import PromptCandidate, PromptStage
from src.evaluation.metrics import evaluate_regex_match

def dspy_metric(example, prediction, trace=None):
    """
    Standard DSPy metric for optimization.
    Returns 1.0 if correct, 0.0 otherwise.
    """
    # example.answer and prediction.answer are expected strings
    # We use evaluate_regex_match for better robustness
    is_correct, _ = evaluate_regex_match(prediction.answer, example.answer)
    return float(is_correct)

def extract_prompt_from_module(module: dspy.Module) -> str:
    """
    Extracts the instructions from the first predictor found in the module.
    For more complex modules, this might need refinement.
    """
    for name, parameter in module.named_predictors():
        return parameter.signature.instructions
    return ""

def optimize_baseline(trainset, strong_model_name: str) -> PromptCandidate:
    """
    Stage 1: Optimize instructions using the strong model.
    """
    strong_lm = get_llm_client(strong_model_name)
    
    # Configure default LM for evaluation
    configure_dspy_lm(strong_lm)
    
    # GEPA optimizer
    # reflection_lm is the one proposing changes (Strong model)
    # default LM is the one being evaluated (Strong model)
    optimizer = GEPA(
        metric=dspy_metric,
        reflection_lm=strong_lm,
        max_full_evals=10,
        candidate_selection_strategy='pareto'
    )
    
    module = QAModule()
    # Ensure dspy.settings is correctly set before compilation
    with dspy.context(lm=strong_lm):
        optimized_module = optimizer.compile(module, trainset=trainset)
    
    prompt_content = extract_prompt_from_module(optimized_module)
    
    return PromptCandidate(
        prompt_id=str(uuid.uuid4()),
        stage=PromptStage.BASELINE,
        content=prompt_content
    )

def harden_prompt(trainset, baseline_prompt: PromptCandidate, strong_model_name: str, weak_model_name: str) -> PromptCandidate:
    """
    Stage 2: Harden the prompt using the weak model for evaluation,
    but the strong model for reflection/optimization.
    """
    strong_lm = get_llm_client(strong_model_name)
    weak_lm = get_llm_client(weak_model_name)
    
    # Initialize a module with the baseline prompt instructions
    module = QAModule()
    # We need to set the instructions of the baseline prompt to the module
    for name, parameter in module.named_predictors():
        parameter.signature = parameter.signature.with_instructions(baseline_prompt.content)
    
    # GEPA optimizer
    # reflection_lm is the one proposing changes (Strong model)
    # default LM is the one being evaluated (Weak model)
    optimizer = GEPA(
        metric=dspy_metric,
        reflection_lm=strong_lm,
        max_full_evals=10,
        candidate_selection_strategy='pareto'
    )
    
    # Ensure evaluation uses the weak model
    with dspy.context(lm=weak_lm):
        hardened_module = optimizer.compile(module, trainset=trainset)
    
    prompt_content = extract_prompt_from_module(hardened_module)
    
    return PromptCandidate(
        prompt_id=str(uuid.uuid4()),
        stage=PromptStage.HARDENED,
        content=prompt_content,
        parent_prompt_id=baseline_prompt.prompt_id
    )

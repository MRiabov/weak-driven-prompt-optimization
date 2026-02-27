from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class PromptStage(str, Enum):
    BASELINE = "BASELINE"
    HARDENED = "HARDENED"

class ExperimentConfig(BaseModel):
    experiment_id: str
    large_model: str
    small_model: str
    benchmarks: List[str]
    budget_iterations: int

class PromptCandidate(BaseModel):
    prompt_id: str
    stage: PromptStage
    content: str
    parent_prompt_id: Optional[str] = None

class EvaluationResult(BaseModel):
    eval_id: str
    prompt_id: str
    benchmark_name: str
    model_used: str
    accuracy: float
    api_cost: float
    duration_seconds: float
    failed_cases: List[Dict[str, Any]]
    dataset_path: Optional[str] = None

class ModelOutputRecord(BaseModel):
    output_id: str
    eval_id: str
    prompt_id: str
    model_used: str
    input_query: str
    raw_output: str
    parsed_answer: str
    expected_answer: str
    is_correct: bool

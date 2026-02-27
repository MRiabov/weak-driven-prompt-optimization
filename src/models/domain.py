from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, ConfigDict


class PromptStage(str, Enum):
    BASELINE = "BASELINE"
    HARDENED = "HARDENED"


class ExperimentConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    experiment_id: str
    large_model: str
    small_model: str
    benchmarks: List[str]
    budget_iterations: int


class PromptCandidate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    prompt_id: str
    stage: PromptStage
    content: str
    parent_prompt_id: Optional[str] = None


class EvaluationResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
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
    model_config = ConfigDict(protected_namespaces=())
    output_id: str
    eval_id: str
    prompt_id: str
    model_used: str
    input_query: str
    raw_output: str
    parsed_answer: str
    expected_answer: str
    is_correct: bool

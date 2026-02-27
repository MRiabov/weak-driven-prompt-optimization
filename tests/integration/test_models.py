from src.models.domain import ExperimentConfig, PromptCandidate, PromptStage

def test_experiment_config():
    config = ExperimentConfig(
        experiment_id="exp-001",
        large_model="gpt-4",
        small_model="gpt-3.5-turbo",
        benchmarks=["math"],
        budget_iterations=5
    )
    assert config.experiment_id == "exp-001"

def test_prompt_candidate():
    prompt = PromptCandidate(
        prompt_id="p-001",
        stage=PromptStage.BASELINE,
        content="Hello world"
    )
    assert prompt.stage == PromptStage.BASELINE
    assert prompt.parent_prompt_id is None

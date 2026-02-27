import pytest
import shutil
from pathlib import Path
from src.runner.state import ExperimentStateManager, ExperimentStatus
from src.models.domain import PromptCandidate, PromptStage, EvaluationResult

@pytest.fixture
def temp_checkpoint_dir(tmp_path):
    return tmp_path / ".checkpoints"

def test_state_manager_initialization(temp_checkpoint_dir):
    exp_id = "test-exp-1"
    manager = ExperimentStateManager(exp_id, max_budget_iterations=10, base_dir=str(temp_checkpoint_dir))
    
    assert manager.experiment_id == exp_id
    assert manager.max_budget_iterations == 10
    assert manager.current_iterations == 0
    assert manager.status == ExperimentStatus.NOT_STARTED
    assert (temp_checkpoint_dir / exp_id).exists()

def test_budget_tracking(temp_checkpoint_dir):
    manager = ExperimentStateManager("test-exp-2", max_budget_iterations=2, base_dir=str(temp_checkpoint_dir))
    
    assert manager.can_continue_optimization() is True
    manager.increment_iteration()
    assert manager.current_iterations == 1
    assert manager.can_continue_optimization() is True
    manager.increment_iteration()
    assert manager.current_iterations == 2
    assert manager.can_continue_optimization() is False

def test_status_persistence(temp_checkpoint_dir):
    exp_id = "test-exp-3"
    manager = ExperimentStateManager(exp_id, max_budget_iterations=5, base_dir=str(temp_checkpoint_dir))
    manager.update_status(ExperimentStatus.STAGE_1_RUNNING)
    
    # Create a new manager instance to simulate reload
    new_manager = ExperimentStateManager(exp_id, max_budget_iterations=5, base_dir=str(temp_checkpoint_dir))
    assert new_manager.status == ExperimentStatus.STAGE_1_RUNNING

def test_candidate_checkpointing(temp_checkpoint_dir):
    exp_id = "test-exp-4"
    manager = ExperimentStateManager(exp_id, max_budget_iterations=5, base_dir=str(temp_checkpoint_dir))
    
    candidate = PromptCandidate(
        prompt_id="p1",
        stage=PromptStage.BASELINE,
        content="Test prompt content"
    )
    
    manager.save_candidate(candidate)
    
    loaded_candidate = manager.load_candidate("p1")
    assert loaded_candidate.prompt_id == candidate.prompt_id
    assert loaded_candidate.content == candidate.content
    assert loaded_candidate.stage == candidate.stage

def test_evaluation_checkpointing(temp_checkpoint_dir):
    exp_id = "test-exp-5"
    manager = ExperimentStateManager(exp_id, max_budget_iterations=5, base_dir=str(temp_checkpoint_dir))
    
    evaluation = EvaluationResult(
        eval_id="e1",
        prompt_id="p1",
        benchmark_name="gsm8k",
        model_used="gpt-3.5-turbo",
        accuracy=0.85,
        api_cost=0.01,
        duration_seconds=1.5,
        failed_cases=[]
    )
    
    manager.save_evaluation(evaluation)
    
    loaded_evaluation = manager.load_evaluation("e1")
    assert loaded_evaluation.eval_id == evaluation.eval_id
    assert loaded_evaluation.accuracy == evaluation.accuracy
    assert loaded_evaluation.model_used == evaluation.model_used

def test_atomic_write_simulation(temp_checkpoint_dir):
    # This test is more of a smoke test for the _atomic_write method
    exp_id = "test-exp-6"
    manager = ExperimentStateManager(exp_id, max_budget_iterations=5, base_dir=str(temp_checkpoint_dir))
    
    file_path = temp_checkpoint_dir / exp_id / "atomic_test.json"
    manager._atomic_write(file_path, '{"test": "data"}')
    
    assert file_path.exists()
    assert file_path.read_text() == '{"test": "data"}'
    assert not file_path.with_suffix(".tmp").exists()

import pytest
from unittest.mock import MagicMock, patch
from src.runner.executors import Stage1Executor, Stage2Executor, Stage3Executor
from src.models.domain import (
    PromptCandidate,
    PromptStage,
    EvaluationResult,
)
from src.runner.state import ExperimentStateManager, ExperimentStatus


@pytest.fixture
def mock_state_manager(tmp_path):
    sm = ExperimentStateManager(
        experiment_id="test_exp", max_budget_iterations=10, base_dir=str(tmp_path)
    )
    return sm


@pytest.fixture
def mock_loader():
    loader = MagicMock()

    def load_side_effect(benchmark, split="test", limit=None):
        data = [
            {"question": "What is 2+2?", "answer": "4"},
            {"question": "What is 5+5?", "answer": "10"},
        ]
        if limit:
            data = data[:limit]
        return iter(data)

    loader.load.side_effect = load_side_effect
    return loader


@pytest.fixture
def mock_exporter():
    exporter = MagicMock()
    exporter.persist_outputs.return_value = "fake/path/to/eval.jsonl"
    return exporter


@patch("src.runner.executors.optimize_baseline")
def test_stage1_executor(mock_optimize, mock_state_manager, mock_loader):
    mock_optimize.return_value = PromptCandidate(
        prompt_id="p1", stage=PromptStage.BASELINE, content="Baseline prompt"
    )

    executor = Stage1Executor(mock_state_manager, "strong-model")
    candidate = executor.execute(mock_loader, "SuperGPQA", limit=2)

    assert candidate.prompt_id == "p1"
    assert mock_state_manager.status == ExperimentStatus.STAGE_1_COMPLETE
    assert mock_state_manager.current_iterations == 1
    mock_optimize.assert_called_once()


@patch("src.runner.executors.harden_prompt")
def test_stage2_executor(mock_harden, mock_state_manager, mock_loader):
    baseline = PromptCandidate(
        prompt_id="p1", stage=PromptStage.BASELINE, content="Baseline"
    )
    mock_harden.return_value = PromptCandidate(
        prompt_id="p2",
        stage=PromptStage.HARDENED,
        content="Hardened prompt",
        parent_prompt_id="p1",
    )

    executor = Stage2Executor(mock_state_manager, "strong-model", "weak-model")
    candidate = executor.execute(mock_loader, "SuperGPQA", baseline, limit=2)

    assert candidate.prompt_id == "p2"
    assert candidate.parent_prompt_id == "p1"
    assert mock_state_manager.status == ExperimentStatus.STAGE_2_COMPLETE
    assert mock_state_manager.current_iterations == 1


@patch("src.runner.executors.get_llm_client")
def test_stage3_executor(mock_get_llm, mock_state_manager, mock_loader, mock_exporter):
    mock_lm = MagicMock()
    mock_get_llm.return_value = mock_lm

    # Mock DSPy module call
    with patch("src.runner.executors.QAModule") as mock_qa_class:
        mock_module = MagicMock()
        mock_module.return_value = MagicMock(answer="4")
        mock_qa_class.return_value = mock_module

        candidate = PromptCandidate(
            prompt_id="p2", stage=PromptStage.HARDENED, content="Hardened"
        )
        executor = Stage3Executor(mock_state_manager, mock_exporter)

        result = executor.execute(
            mock_loader, "SuperGPQA", candidate, "eval-model", limit=1
        )

        assert isinstance(result, EvaluationResult)
        assert result.prompt_id == "p2"
        assert result.accuracy == 1.0
        assert mock_state_manager.base_dir.joinpath(
            "evaluations", f"{result.eval_id}.json"
        ).exists()
        mock_exporter.persist_outputs.assert_called_once()

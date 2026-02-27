import pytest
import shutil
from unittest.mock import patch
from src.models.domain import ExperimentConfig, PromptCandidate, PromptStage
from src.runner.orchestrator import ExperimentRunner
from src.runner.state import ExperimentStatus


@pytest.fixture
def temp_checkpoint_dir(tmp_path):
    d = tmp_path / "checkpoints"
    d.mkdir()
    yield d
    if d.exists():
        shutil.rmtree(d)


def test_runner_initialization(temp_checkpoint_dir):
    with (
        patch("src.runner.orchestrator.init_langfuse"),
        patch("src.runner.orchestrator.setup_dspy_tracing"),
    ):
        config = ExperimentConfig(
            experiment_id="test_exp",
            large_model="gpt-4o",
            small_model="gpt-4o-mini",
            benchmarks=["gsm8k"],
            budget_iterations=5,
        )
        runner = ExperimentRunner(config)

        assert runner.config == config
        assert runner.state_manager.experiment_id == "test_exp"
        assert runner.state_manager.status == ExperimentStatus.NOT_STARTED


def test_runner_full_flow_mocked(temp_checkpoint_dir):
    mock_baseline = PromptCandidate(
        prompt_id="p1", stage=PromptStage.BASELINE, content="baseline"
    )
    mock_hardened = PromptCandidate(
        prompt_id="p2", stage=PromptStage.HARDENED, content="hardened"
    )

    config = ExperimentConfig(
        experiment_id="test_exp_full",
        large_model="gpt-4o",
        small_model="gpt-4o-mini",
        benchmarks=["gsm8k"],
        budget_iterations=5,
    )

    with (
        patch("src.runner.orchestrator.init_langfuse"),
        patch("src.runner.orchestrator.setup_dspy_tracing"),
        patch("src.runner.state.ExperimentStatus", ExperimentStatus),
    ):  # Ensure enum is real
        runner = ExperimentRunner(config)
        runner.state_manager.base_dir = temp_checkpoint_dir / "test_exp_full"
        runner.state_manager.base_dir.mkdir(parents=True, exist_ok=True)
        runner.state_manager._state_file = runner.state_manager.base_dir / "state.json"

        def side_effect_stage1(*args, **kwargs):
            runner.state_manager.status = ExperimentStatus.STAGE_1_COMPLETE
            return mock_baseline

        def side_effect_stage2(*args, **kwargs):
            runner.state_manager.status = ExperimentStatus.STAGE_2_COMPLETE
            return mock_hardened

        with (
            patch(
                "src.runner.executors.Stage1Executor.execute",
                side_effect=side_effect_stage1,
            ) as m1,
            patch(
                "src.runner.executors.Stage2Executor.execute",
                side_effect=side_effect_stage2,
            ) as m2,
            patch("src.runner.executors.Stage3Executor.execute") as m3,
        ):
            result = runner.run()

            assert result["status"] == ExperimentStatus.COMPLETE.value
            assert m1.called
            assert m2.called
            assert m3.call_count == 2

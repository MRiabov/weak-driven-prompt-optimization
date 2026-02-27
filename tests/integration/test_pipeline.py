import yaml
import pytest
from unittest.mock import patch
from main import run_experiment, main as cli_main
from tests.mock_llm import MockLLM


@pytest.fixture
def mock_config_path(tmp_path):
    config = {
        "experiment_id": "test-integration-001",
        "large_model": "mock-strong",
        "small_model": "mock-weak",
        "benchmarks": ["FRONTIERMATH"],
        "budget_iterations": 2,
    }

    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config, f)

    return str(config_file)


@patch("src.runner.orchestrator.DatasetLoader")
@patch("src.optimization.optimizer.get_llm_client")
@patch("src.runner.executors.get_llm_client")
def test_experiment_pipeline(
    mock_get_llm_exec,
    mock_get_llm_opt,
    mock_loader_exec,
    mock_config_path,
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "dummy")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "dummy")
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    # Setup mock LLM
    mock_llm = MockLLM(
        responses=[
            '{"reasoning": "R1", "answer": "A1"}',
            '{"reasoning": "R2", "answer": "A2"}',
            '{"reasoning": "R3", "answer": "A3"}',
            '{"reasoning": "R4", "answer": "A4"}',
        ]
        * 10
    )
    mock_get_llm_exec.return_value = mock_llm
    mock_get_llm_opt.return_value = mock_llm

    # Setup mock dataset loader
    mock_data = [{"question": "Q1", "answer": "A1"}, {"question": "Q2", "answer": "A2"}]

    # Ensure the loader returns the mock data
    mock_loader_instance = mock_loader_exec.return_value
    mock_loader_instance.load.return_value = mock_data

    # Run experiment
    run_experiment(mock_config_path)

    # Verify checkpoints
    assert (tmp_path / ".checkpoints" / "test-integration-001" / "state.json").exists()

    # Verify Report Generation
    # We can call the reporting engine or the CLI for report
    import sys

    # Mock sys.argv for the report command
    test_args = [
        "main.py",
        "report",
        "--experiment-id",
        "test-integration-001",
        "--output",
        str(tmp_path / "report.md"),
    ]
    with patch.object(sys, "argv", test_args):
        cli_main()

    # Check that report was generated
    # Check that report was generated and has content
    assert (tmp_path / "report.md").exists()
    report_content = (tmp_path / "report.md").read_text()
    assert "# Experiment Report: test-integration-001" in report_content
    # Each prompt should have 2 evaluations (1 for small_model, 1 for large_model)
    # The reporter aggregates them.
    assert "Evaluations Count: 2" in report_content
    assert "The weak-hardened prompt performed identically" in report_content

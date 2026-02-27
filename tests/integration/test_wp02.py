import pytest
import os
import json
from unittest.mock import MagicMock, patch
from src.evaluation.loaders import DatasetLoader
from src.evaluation.metrics import evaluate_exact_match, evaluate_regex_match
from src.evaluation.exporter import DatasetExporter
from src.models.domain import ModelOutputRecord

@patch("src.evaluation.loaders.load_dataset")
def test_dataset_loader_streaming(mock_load):
    # Mocking the dataset object
    mock_data = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "What is 3+3?", "answer": "6"}
    ]
    
    mock_ds = MagicMock()
    # Mocking split access ds['train'] or similar
    mock_ds.__getitem__.return_value = iter(mock_data)
    mock_ds.keys.return_value = ["train"]
    mock_load.return_value = mock_ds
    
    records = list(DatasetLoader.load("FRONTIERMATH", limit=2))
    
    assert len(records) == 2
    assert records[0]["question"] == "What is 2+2?"
    assert records[0]["answer"] == "4"

def test_metrics():
    # Exact match
    is_correct, parsed = evaluate_exact_match("4", "4")
    assert is_correct is True
    
    is_correct, parsed = evaluate_exact_match(" 4 \n", "4")
    assert is_correct is True
    
    # Regex match
    raw = "Thought: ... Final Answer: 42"
    is_correct, parsed = evaluate_regex_match(raw, "42")
    assert is_correct is True
    assert parsed == "42"
    
    is_correct, parsed = evaluate_regex_match("No answer here", "42")
    assert is_correct is False

def test_dataset_exporter(tmp_path):
    exporter = DatasetExporter()
    eval_id = "test-eval"
    output_dir = str(tmp_path)
    
    records = [
        ModelOutputRecord(
            output_id="o1",
            eval_id=eval_id,
            prompt_id="p1",
            model_used="m1",
            input_query="q1",
            raw_output="a1",
            parsed_answer="a1",
            expected_answer="a1",
            is_correct=True
        )
    ]
    
    file_path = exporter.persist_outputs(eval_id, iter(records), output_dir)
    
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        data = json.loads(f.readline())
        assert data["output_id"] == "o1"
        assert data["is_correct"] is True

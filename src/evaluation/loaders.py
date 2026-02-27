import os
from typing import Iterator, Dict, Any, List
from datasets import load_dataset

class DatasetLoader:
    """
    Unified loader for benchmarks using HuggingFace datasets streaming.
    """
    
    DATASET_MAPPING = {
        "FRONTIERMATH": "metr-evals/daft-math",  # Placeholder as FrontierMath is private
        "SuperGPQA": "m-a-p/SuperGPQA",
        "tau^2-Bench": "HuggingFaceH4/tau2-bench-data"
    }

    @classmethod
    def load(cls, benchmark_name: str, split: str = "test", limit: int = None) -> Iterator[Dict[str, Any]]:
        """
        Loads a dataset in streaming mode and yields standardized records.
        """
        dataset_path = cls.DATASET_MAPPING.get(benchmark_name)
        if not dataset_path:
            raise ValueError(f"Unknown benchmark: {benchmark_name}. Available: {list(cls.DATASET_MAPPING.keys())}")

        # Note: Some datasets might require specific configurations or splits.
        # This implementation assumes a general 'test' split or default.
        try:
            ds = load_dataset(dataset_path, streaming=True)
            
            # Use requested split if available, otherwise fallback to first available split
            if split in ds:
                data = ds[split]
            else:
                # Fallback to 'train' or first split
                available_splits = list(ds.keys())
                if not available_splits:
                    raise RuntimeError(f"No splits found for dataset {dataset_path}")
                data = ds[available_splits[0]]

            count = 0
            for record in data:
                if limit and count >= limit:
                    break
                
                std_record = cls._standardize(benchmark_name, record)
                if std_record["question"]: # Skip empty records if any
                    yield std_record
                    count += 1
                
        except Exception as e:
            if "gated" in str(e).lower() or "authenticated" in str(e).lower():
                 # For gated datasets, we might want to yield a mock or informative error
                 # but for this experiment, we'll just raise a clearer error.
                 raise RuntimeError(f"Dataset {dataset_path} is gated. Please run 'huggingface-cli login' or use an authorized token.") from e
            raise RuntimeError(f"Failed to load dataset {benchmark_name} from {dataset_path}: {e}")

    @staticmethod
    def _standardize(benchmark_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardizes records into {"question": "...", "answer": "..."}.
        """
        if benchmark_name == "FRONTIERMATH":
            # metr-evals/daft-math schema: original_question, updated_answer, answer
            question = record.get("original_question") or record.get("updated_question") or record.get("question")
            answer = record.get("updated_answer") or record.get("answer")
            return {
                "question": str(question) if question else "",
                "answer": str(answer) if answer else ""
            }
        elif benchmark_name == "SuperGPQA":
            # m-a-p/SuperGPQA schema: question, options, answer, answer_letter
            question = record.get("question")
            options = record.get("options")
            if options and isinstance(options, list):
                options_str = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
                question = f"{question}\n\nOptions:\n{options_str}"
            
            answer = record.get("answer_letter") or record.get("label") or record.get("answer")
            return {
                "question": str(question) if question else "",
                "answer": str(answer) if answer else ""
            }
        elif benchmark_name == "tau^2-Bench":
            # HuggingFaceH4/tau2-bench-data schema is complex (nested)
            # We try to extract user instructions as the question
            user_scenario = record.get("user_scenario", {})
            instructions = user_scenario.get("instructions", {})
            question = instructions.get("task_instructions") or record.get("question")
            
            # If still nothing, try to see if it's a flatter record
            if not question:
                 question = record.get("user_query") or record.get("instruction")
            
            # For answer, we might use the evaluation_criteria as a string representation
            eval_criteria = record.get("evaluation_criteria")
            answer = str(eval_criteria) if eval_criteria else record.get("answer")
            
            return {
                "question": str(question) if question else "",
                "answer": str(answer) if answer else ""
            }
        
        return {
            "question": str(record.get("question") or ""),
            "answer": str(record.get("answer") or "")
        }

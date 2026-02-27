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
                # Fallback to 'train' if 'test' is not available in streaming for some reason
                # or just use the first split
                first_split = list(ds.keys())[0]
                data = ds[first_split]

            count = 0
            for record in data:
                if limit and count >= limit:
                    break
                
                yield cls._standardize(benchmark_name, record)
                count += 1
                
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset {benchmark_name} from {dataset_path}: {e}")

    @staticmethod
    def _standardize(benchmark_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardizes records into {"question": "...", "answer": "..."}.
        """
        if benchmark_name == "FRONTIERMATH":
            # metr-evals/daft-math has 'question' and 'answer'
            return {
                "question": record.get("question"),
                "answer": record.get("answer")
            }
        elif benchmark_name == "SuperGPQA":
            # SuperGPQA has 'question' and 'correct_answer'
            return {
                "question": record.get("question"),
                "answer": record.get("correct_answer")
            }
        elif benchmark_name == "tau^2-Bench":
            # tau2-bench-data might have different structure. 
            # Assuming it has 'user_query' or similar based on research.
            # I'll default to looking for common keys.
            return {
                "question": record.get("user_query") or record.get("instruction") or record.get("question"),
                "answer": record.get("reference_answer") or record.get("answer")
            }
        
        return {
            "question": record.get("question"),
            "answer": record.get("answer")
        }

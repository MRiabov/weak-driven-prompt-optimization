import json
import os
from typing import Iterator
from src.models.domain import ModelOutputRecord

class DatasetExporter:
    """
    Handles persisting model outputs to JSONL format.
    """
    
    def persist_outputs(self, eval_id: str, records: Iterator[ModelOutputRecord], output_dir: str) -> str:
        """
        Persists the model output records to a dataset format (e.g., JSONL) and returns the file path.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        file_path = os.path.join(output_dir, f"eval_{eval_id}.jsonl")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for record in records:
                # Use model_dump() for Pydantic v2
                line = json.dumps(record.model_dump())
                f.write(line + '\n')
                
        return file_path

import re
from typing import Tuple, Optional

def evaluate_exact_match(raw_output: str, expected_answer: str) -> Tuple[bool, str]:
    """
    Checks if the expected answer is exactly present in the raw output or matches after stripping.
    """
    # Simple extraction: try to find the answer in the last part of the output or just clean it.
    parsed_answer = raw_output.strip()
    
    # If the expected answer is in the parsed answer, consider it correct for EM in some contexts,
    # but strictly EM should be exact. 
    # Let's do a cleaned EM.
    cleaned_parsed = parsed_answer.lower()
    cleaned_expected = expected_answer.strip().lower()
    
    is_correct = cleaned_parsed == cleaned_expected
    
    return is_correct, parsed_answer

def evaluate_regex_match(raw_output: str, expected_answer: str, pattern: str = r"Final Answer:\s*(.*)") -> Tuple[bool, str]:
    """
    Extracts an answer using regex and compares with expected.
    """
    match = re.search(pattern, raw_output, re.IGNORECASE | re.DOTALL)
    if match:
        parsed_answer = match.group(1).strip()
    else:
        # Fallback to the whole output if pattern not found
        parsed_answer = raw_output.strip()

    cleaned_parsed = parsed_answer.lower()
    cleaned_expected = expected_answer.strip().lower()
    
    is_correct = cleaned_expected in cleaned_parsed or cleaned_parsed == cleaned_expected
    
    return is_correct, parsed_answer

def get_evaluator(benchmark_name: str):
    """
    Returns the appropriate evaluation function for the benchmark.
    """
    if benchmark_name in ["FRONTIERMATH", "SuperGPQA"]:
        return evaluate_regex_match
    return evaluate_exact_match

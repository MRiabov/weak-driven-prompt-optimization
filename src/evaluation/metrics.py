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

def evaluate_regex_match(raw_output: str, expected_answer: str, pattern: Optional[str] = None) -> Tuple[bool, str]:
    """
    Extracts an answer using regex and compares with expected.
    Supports several common formats (e.g. boxed answers, Final Answer markers).
    """
    if pattern:
        patterns = [pattern]
    else:
        # Priority order for extraction patterns
        patterns = [
            r"\\boxed\{(.*?)\}",                    # LaTeX boxed answer
            r"Final Answer:\s*(.*)",              # Explicit Final Answer label
            r"The answer is:\s*(.*)",             # Common answer prompt
            r"####\s*(.*)",                       # GSM8K-style separator
        ]

    parsed_answer = ""
    for pat in patterns:
        match = re.search(pat, raw_output, re.IGNORECASE | re.DOTALL)
        if match:
            # If multiple matches, we take the LAST one as models often reason and then conclude.
            all_matches = re.findall(pat, raw_output, re.IGNORECASE | re.DOTALL)
            parsed_answer = all_matches[-1].strip()
            break
    
    if not parsed_answer:
        # Fallback to the last line if it's not too long, or the whole thing
        lines = raw_output.strip().split("\n")
        if lines:
            last_line = lines[-1].strip()
            if len(last_line) < 100:
                parsed_answer = last_line
            else:
                parsed_answer = raw_output.strip()
    
    # Normalization for comparison
    cleaned_parsed = parsed_answer.lower().replace(",", "").replace("$", "").strip()
    cleaned_expected = expected_answer.strip().lower().replace(",", "").replace("$", "")
    
    # We want to be lenient: if expected is in parsed, or if they are equal
    is_correct = (cleaned_expected == cleaned_parsed) or (f" {cleaned_expected}" in f" {cleaned_parsed} ")
    
    return is_correct, parsed_answer

def get_evaluator(benchmark_name: str):
    """
    Returns the appropriate evaluation function for the benchmark.
    """
    if benchmark_name in ["FRONTIERMATH", "SuperGPQA"]:
        # Use regex for structured extraction
        return evaluate_regex_match
    return evaluate_exact_match

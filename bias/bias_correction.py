from llm_api import Prompt
import os

# Read the system prompt from file
prompt_file_path = os.path.join(os.path.dirname(__file__), "bias_correction_prompt.txt")
with open(prompt_file_path, "r") as f:
    SYSTEM_PROMPT = f.read()

def correct_bias(text):
    """
    Uses the Prompt API to correct bias in the given text.
    Returns the unbiased replacement and the reason it was biased.
    """
    chat = Prompt(system_message=SYSTEM_PROMPT)
    response = chat.prompt(text)

    # Parse the response (expecting format: unbiased text\nreason)
    lines = response.strip().split('\n', 1)
    unbiased_replacement = lines[0] if len(lines) > 0 else ""
    reason_biased = lines[1] if len(lines) > 1 else ""

    return unbiased_replacement, reason_biased

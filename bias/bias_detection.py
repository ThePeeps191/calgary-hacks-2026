from llm_api import Prompt
import os

# Read the system prompt from file
prompt_file_path = os.path.join(os.path.dirname(__file__), "bias_detection_prompt.txt")
with open(prompt_file_path, "r") as f:
    SYSTEM_PROMPT = f.read()

# Initialize the Prompt API with system prompt
chat = Prompt(system_message=SYSTEM_PROMPT)

def is_text_biased_enough(text):
    """
    Uses the Prompt API to determine if the given text is biased enough to warrant correction.
    Returns True if biased, False otherwise.
    """
    response = chat.prompt(text)
    
    # Parse the response (expecting "true" or "false")
    return response.strip().lower() == "true"
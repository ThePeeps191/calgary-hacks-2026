from llm_api import Prompt
import os

# Read the system prompt from file
prompt_file_path = os.path.join(os.path.dirname(__file__), "bias_score_prompt.txt")
with open(prompt_file_path, "r") as f:
    SYSTEM_PROMPT = f.read()

def return_biased_score(text):
    chat = Prompt(system_message=SYSTEM_PROMPT)
    response = chat.prompt(text)
    
    score, reasoning = -1, []
    print(response)
    for i in response.split("\n"):
        if i.startswith("\"Score\":"):
            score = int(i.split(":")[1].strip())
        elif i.startswith("\"Reasoning\":"):
            reasoning.append(i.split(":")[1].strip())
    return score, reasoning

import google.generativeai as genai
from dotenv import load_dotenv
import os

print("finished importing gemini")

# .env gemini key
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY is None:
    raise ValueError("GEMINI_KEY is not set in the environment!")
print(f"Gemini key: {GEMINI_KEY[:5]}")
genai.configure(api_key=GEMINI_KEY)

class Prompt:
    def __init__(self, system_message=None):
        self.messages = []
        self.system_message = system_message
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction=system_message if system_message else None
        )
    
    def prompt(self, user_input):
        try:
            self.messages.append({"role": "user", "content": user_input})
            
            # Build conversation history for Gemini
            history = []
            for msg in self.messages:
                history.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })
            
            # Create chat session with history
            chat = self.model.start_chat(history=history[:-1] if history else [])
            response = chat.send_message(user_input)
            
            assistant_message = response.text
            self.messages.append({"role": "assistant", "content": assistant_message})

            return assistant_message
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        if self.messages and self.messages[0]["role"] == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []

if __name__ == "__main__":
    chat = Prompt()
    response1 = chat.prompt("What is 1 + 1?")
    print(response1)
    response2 = chat.prompt("What is 3 plus the answer to the previous question?")
    print(response2)
    response3 = chat.prompt("What is 5 times the answer to the previous question, plus the answer to the previous previous question?")
    print(response3)
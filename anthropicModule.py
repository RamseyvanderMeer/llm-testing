import anthropic
from dotenv import load_dotenv
import os

class anthropicLLM:
    def __init__(self):
        self.prompt = os.getenv("anthropic_prompt")
        self.client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        self.name = "anthropic"

    def get_response(self, prompt, model="claude-3-opus-20240229"):
        message = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.0,
            system="Respond to user input to the best of your ability.",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        return message.conten[0].text
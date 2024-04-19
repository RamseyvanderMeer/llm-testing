from openai import OpenAI
from dotenv import load_dotenv
import os


class openai35LLM:
    def __init__(self):
        self.prompt = os.getenv("openai_prompt")
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.name = "openai-gpt-3.5"

    def get_response(self, prompt, model="gpt-3.5-turbo-0125"):
        response = self.client.chat.completions.create(
            model=model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.0,
        )

        return response.choices[0].message.content

class openai4LLM:
    def __init__(self):
        self.prompt = os.getenv("openai_prompt")
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.name = "openai-gpt-4"

    def get_response(self, prompt, model="gpt-4-turbo"):
        response = self.client.chat.completions.create(
            model=model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.0,
        )

        return response.choices[0].message.content
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from llamaapi import LlamaAPI
from dotenv import load_dotenv
import os

load_dotenv()

prompt = os.getenv("prompt")

api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content=prompt.format("eight'oclock each sunday, exept for the second sunday of the month where it opens at 10:00 am", "response need to be in the format of a time, e.g. 8:00 am, 10:00 pm, 12:00 pm, etc. which matches the regex pattern ^[0-9]{1,2}:[0-9]{2} [ap]m$. No other format is accepted and other context is unessasary. Remove all context that is not needed and doesn't match the regex."))
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)

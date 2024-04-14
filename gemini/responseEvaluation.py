import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

prompt = os.getenv("prompt")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(prompt.format("eight'oclock each sunday, exept for the second sunday of the month where it opens at 10:00 am", "response need to be in the format of a time, e.g. 8:00 am, 10:00 pm, 12:00 pm, etc. which matches the regex pattern ^[0-9]{1,2}:[0-9]{2} [ap]m$. No other format is accepted and other context is unessasary. Remove all context that is not needed and doesn't match the regex."))

print(response.text)

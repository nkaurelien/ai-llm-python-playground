import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt="Traduisez le texte suivant en français: 'Hello, World!'",
  max_tokens=60
)

generated_text = response.choices[0].text
print(generated_text)
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurez votre clé API
openai.api_key = os.getenv('OPENAI_API_KEY')


completion = openai.ChatCompletion.create(
  model="ft:gpt-3.5-turbo-0613:smart-data-pay:labourlaw-31qa:85vpuC37",
  messages=[
    # {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Quelle est la procédure pour un licenciement pour faute grave?"}
  ]
)
print(completion.choices[0].message)
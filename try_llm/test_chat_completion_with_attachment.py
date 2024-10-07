# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

file_upload_response = openai.File.create(
    file=open("chemin/vers/votre/fichier.txt", "rb")
)

file_id = file_upload_response.id

response = openai.Completion.create(
    engine="text-davinci-003", # Remplacer par le nom correct de l'engine si nécessaire
    prompt={
        "file": {
            "id": file_id,
            "filename": "votre/fichier.txt"
        },
        "model": "code-interpreter",
        "examples": [["Python code example", "Translated code example"]], # Fournir des exemples pertinents
        "task": "Translate the following Python code to Java"
    },
    max_tokens=500
)

generated_text = response.choices[0].text
print(generated_text)
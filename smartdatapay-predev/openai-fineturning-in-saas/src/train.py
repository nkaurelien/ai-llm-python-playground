import openai
import os
from dotenv import load_dotenv

load_dotenv()


# Configurez votre clé API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Chemin des fichiers
cwd = os.getcwd()
output_jsonl_path = os.path.join(cwd, 'data/law_data_dialogs.jsonl')

def finturning():


    # 1. Téléversez votre fichier de données
    with open(output_jsonl_path, 'rb') as file:
        data_upload_response = openai.File.create(
            file=file,
            purpose='fine-tune'
        )

    training_file_id = data_upload_response.id
    print(data_upload_response)

    # 2. Créez un job d'entraînement
    training_response = openai.FineTuningJob.create(
        model="gpt-3.5-turbo",
        training_file=training_file_id,
        suffix='labourlaw_31qa',
        # hyperparameters={'n_epochs': 3}
    )


    openai.FineTuningJob.list(limit=10)

    print(training_response)
    return
    # Récupérez l'ID du job d'entraînement pour suivre la progression ou obtenir le modèle adapté
    training_job_id = training_response.id
    print(training_job_id)





finturning()
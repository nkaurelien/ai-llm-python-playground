import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Chemin des fichiers
cwd = os.getcwd()
input_csv_path = os.path.join(cwd, 'data/qn_law_validated - Feuille 1.csv')
output_jsonl_path = os.path.join(cwd, 'data/law_data_dialogs.jsonl')
output_base_jsonl_path = os.path.join(cwd, 'data/law_data_dialogs-prompt-completion.jsonl')

# 1. Lire le fichier CSV
law_data = pd.read_csv(input_csv_path)

# 2. Transformer les données
system_message = {
    'role': 'system',
    'content': 'Tu es un systeme expert ou encore un assistant utile sur le Code du travail numérique en france'
}

dialogs = []
dialogs2 = []

for index, row in law_data.iterrows():
    user_message = {
        'role': 'user',
        'content': row['prompt']
    }
    assistant_message = {
        'role': 'assistant',
        'content': row['completion']
    }
    
    dialogue = [system_message, user_message, assistant_message]
    updated_dialog = {"messages": dialogue}
    dialogs.append(updated_dialog)
    
    dialogs2.append({ 'prompt': row['prompt'], 'completion': row['completion']})



# 3. Enregistrer les données au format JSONL
with open(output_jsonl_path, 'w') as file:
    for dialogue in dialogs:
        file.write(json.dumps(dialogue) + '\n')

with open(output_base_jsonl_path, 'w') as file:
    for dialogue in dialogs2:
        file.write(json.dumps(dialogue) + '\n')

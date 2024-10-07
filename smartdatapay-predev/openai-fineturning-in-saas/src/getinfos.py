import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

cwd =  os.getcwd()
output_jsonl_path = os.path.join(cwd, 'data/infos.json')

# Configurez votre clé API
openai.api_key = os.getenv('OPENAI_API_KEY')


# openai.Model.list()
infos =  {
    'FineTuningJobs': openai.FineTuningJob.list(limit=10),
    'Files': openai.File.list(),
}
with open(output_jsonl_path, 'w') as file:
    file.write(json.dumps(infos, indent=True) + '\n')
import openai
import os
from dotenv import load_dotenv
import gradio as gr
import requests
import json

load_dotenv()


# Configurez votre clé API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Chemin des fichiers
cwd = os.getcwd()


defaults = {
    # "model_name":"gpt-3.5-turbo"
    "model_name":"gpt-4"
}

models_by_topics = {
    "laborlaw": "ft:gpt-3.5-turbo-0613:smart-data-pay:labourlaw-31qa:85vpuC37",
    "ccn": "",
    "simu": ""
}

base_prompt = """Vous êtes un assistant utile.
Tu prends en compte les textes et lois du pays la France pour repondre aux questions.
Tu es un expert en calcul de fiche de paie et en droit du travail en france.
Demande moi les informations neccessaires pour une réponse plus précise. Les unes après les autres dans plusieurs messages"""

# base_prompt = "Vous êtes un assistant utile."
#-----------------------------


def chatbot(input_text):

    ### ask to azure

    url = "https://sdp-lang-instance-1.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=SmartDataPayQnA&api-version=2021-10-01&deploymentName=test"

    payload = json.dumps({
    "question": input_text
    })
    headers = {
    'Ocp-Apim-Subscription-Key': os.getenv('AZURE_COGNITIVE_SERVICE_CQA_SUBSCRIPTION_KEY'),
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.getenv('AZURE_COGNITIVE_SERVICE_CQA_SECRET_KEY')
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)


    assistant_answer = data["answers"][0]['answer']
    topic = data["answers"][0]['metadata']['topic']


    ### ask to open ia
    
    # model = models_by_topics[topic] or defaults["model_name"]
    model = "gpt-4"

    completion = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": base_prompt},
        # {"role": "user", "content": input_text},
        # {"role": "assistant", "content": assistant_answer},
        {"role": "user", "content": assistant_answer + "\n\n" + input_text},
        # {"role": "user", "content": "Demande moi les informations neccessaires pour une réponse plus précise. Les unes après les autres dans plusieurs messages"},
    ]
    )
    # print(completion.choices[0].message)


    return completion.choices[0].message.content


def ask_bot_web_interface():

    iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=4, label="Entrer votre texte"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")
    iface.launch(share=True)


#------ Main ---------------


ask_bot_web_interface()
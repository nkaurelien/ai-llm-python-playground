from langchain import OpenAI
from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex,readers, GPTSimpleVectorIndex, PromptHelper
from llama_index import LLMPredictor, ServiceContext
import sys
#from google.colab import drive
import os

# os.environ["OPENAI_API_KEY"] = ''
from dotenv import load_dotenv

load_dotenv()

input_index = os.getenv('INPUT_INDEX', default='index.json') 

# Vérifier si le fichier n'existe pas
if not os.path.exists(input_index):
    # Créer le fichier
    with open(input_index, 'w') as f:
        # Éventuellement initialiser le fichier avec du contenu. Par exemple :
        f.write("{}")  # Initialise avec un objet JSON vide


def construct_index(directory_path):
  # set maximum input size
  max_input_size = 4096
  # set number of output tokens
  num_outputs = 256 * 2
  # set maximum chunk overlap
  max_chunk_overlap = 20
  # set chunk size limit
  chunk_size_limit = 600

  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

  # define LLM
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
  
  documents = SimpleDirectoryReader(directory_path).load_data()
  
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
  index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
  
  index.save_to_disk(input_index)
  
  return index


def ask_bot():
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  while True:
    query = input('What do you want to ask the bot?   \n')
    response = index.query(query, response_mode="compact")
    print ("\nBot says: \n\n" + response.response + "\n\n\n")
    
    

import gradio as gr

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk(input_index)
    # response = index.query(input_text, response_mode="compact")
    response = index.query(input_text)
    return response.response


def ask_bot_web_interface():

    iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=4, label="Entrer votre texte"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")
    iface.launch(share=True)



# -------- Main -----------

docs_path = os.getenv("KNOWLEDGE_BASE_PATH", default="/content/")
index = construct_index(docs_path)

# ask_bot()
ask_bot_web_interface()
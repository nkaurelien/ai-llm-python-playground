from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

input_index = os.getenv('INPUT_INDEX') 

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk(input_index)
    # response = index.query(input_text, response_mode="compact")
    response = index.query(input_text)
    return response.response


def ask_ai():

    iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=4, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")
    iface.launch(share=True)

def ask_ai_shell():

    index = GPTSimpleVectorIndex.load_from_disk(input_index)
    while True: 
        query = input("What do you want to ask? ")
        response = index.query(query)
        display(Markdown(f"Response: <b>{response.response}</b>"))


ask_ai()
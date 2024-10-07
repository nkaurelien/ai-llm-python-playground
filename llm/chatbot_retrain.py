from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
# from IPython.display import Markdown, display
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

input_index = os.getenv('INPUT_INDEX') 


def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600 


    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)


    temperature = os.getenv('OPENAI_TEMPATURE') 
    model_name = os.getenv('OPENAI_API_MODEL') 

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=temperature, model_name=model_name, max_tokens=num_outputs))
 
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk(input_index)

    return index

docs_path = os.getenv("KNOWLEDGE_BASE_PATH")
construct_index(docs_path)

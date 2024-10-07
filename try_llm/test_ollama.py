   
import ollama
import gradio as gr

def greet(prompt):

    # model = 'llama2'
    # model="llama2-uncensored:latest"
    # model = 'gemma:2b'
    model = 'gemma:7b'
    # model = 'mistral'
    
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    # print(response['message']['content'])

    return response['message']['content']

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_API_MODEL")

completion = openai.ChatCompletion.create(
  model=openai_model,
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

if len(completion.choices) > 0:
    print(completion.choices)
    # assert completion.id
    # assert completion.object == "chat.completion.chunk"
    # assert completion.created
    # assert completion.model
    # assert completion.choices[0].finish_reason
    # assert completion.choices[0].index is not None
    # assert completion.choices[0].message.content
    # assert completion.choices[0].message.role
    # for c in completion.choices:
    #     assert c.index is not None
    #     assert c.delta is not None
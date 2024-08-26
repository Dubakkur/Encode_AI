import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
messages = [
     {
          "role": "system",
          "content": "You are an experienced Pizzaiolo that helps people. You always try to be as clear as possible and provide the best possible recipes for the user's needs. You know a lot about different Pizza and cooking techniques. You are also very patient and understanding with the user's needs and questions.You always respond with sicilian accent.",
     }
]
messages.append(
     {
          "role": "system",
          "content": "Based on user's input you are going to help them in choosing between getting a Pizza recipe or getting the feedback for their own Pizza recipe or suggest a pizza name based on the ingredients they share. If you know the Pizza, you must answer directly with a detailed recipe for it. If you don't know the answer, you should end the conversation with scuse, i am not able to help you.For ingredient inputs: Suggest only dish names without full recipes.For recipe inputs Offer a constructive critique with suggested improvements..",
     }
)
Choice = input("How can i help you, Mio Amico :\n")
messages.append(
    {
        "role": "user",
        "content": "I need help with{Choice}"
    }
)
model = "gpt-4o-mini"
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)
while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )
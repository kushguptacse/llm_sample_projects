from llm import call_chat_api
import gradio as gr
import json

messages = []
system_prompt = """You are a helpful assistant for an Airline called FlyAirline.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, just say I don't know. """
messages.append({"role": "system", "content": f"{system_prompt}"})

ticket_dict = {"new york": 500, "london": 600, "paris": 700}

def get_ticket_price(destination):
    return ticket_dict.get(destination.lower(), f"{destination} destination not yet supported!!!!")

def chat_response(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages.append({"role": "user", "content": f"{message}"})
    response = call_chat_api(messages)
    messages.append({"role": "assistant", "content": f"{response.choices[0].message.content}"})
    return response.choices[0].message.content

chat = gr.ChatInterface(fn=chat_response, title="FlyAirline Chatbot Agent")
chat.launch()
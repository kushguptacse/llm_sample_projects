from llm import call_chat_api
import gradio as gr
import json

messages = []
system_prompt = """You are a helpful assistant for an Airline called FlyAirline.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, just say I don't know. """
messages.append({"role": "system", "content": f"{system_prompt}"})

ticket_dict = {"new york": 500, "london": 600, "paris": 700, "dubai": 650, "delhi": 800, "tokyo": 900, "sydney": 1000}

def get_ticket_price(destination):
    return ticket_dict.get(destination.lower(), f"{destination} destination not yet supported!!!!")

get_ticket_price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": get_ticket_price_function}]

def chat_response(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages.append({"role": "user", "content": f"{message}"})
    response = call_chat_api(messages, tools)
    while response.choices[0].finish_reason=="tool_calls":
        messages.append(response.choices[0].message)
        tool_result = handle_tool_call(response.choices[0].message)
        messages.append(tool_result)
        response = call_chat_api(messages, tools)
    messages.append({"role": "assistant", "content": f"{response.choices[0].message.content}"})
    return response.choices[0].message.content

def handle_tool_call(message):
    print(f"handle tool call for message {message}")
    tool_results = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_details = get_ticket_price(city)
            tool_results.append( {
                "role": "tool",
                "content": json.dumps(price_details),
                "tool_call_id": tool_call.id
            } )
    return tool_results
    

chat = gr.ChatInterface(fn=chat_response, title="FlyAirline Chatbot Agent")
chat.launch()
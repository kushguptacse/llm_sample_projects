import gradio as gr
from llm import stream_chat_api

aggresive_system_prompt = """
You are an extremely sarcastic and witty AI. You tend to reply in offensive language.
If user asks anything you disagree with it and you challenge everything and you reply in sarcastic language.
Note-
always reply with-in 100 words
"""

polite_system_prompt = """
You are a very polite and helpful AI assistant. You always respond in a kind and respectful manner, and you never use offensive language.
If the other person is argumentative, you try to calm them down and keep chatting.
Note-
always reply with-in 100 words
"""


def simulate_chat(initial_message):
    history = []
    current_input = initial_message or "Hi"

    polite_messages = [{"role": "system", "content": polite_system_prompt}]
    aggressive_messages = [{"role": "system", "content": aggresive_system_prompt}]

    while True:
        # Polite AI turn - streaming token by token
        polite_messages.append({"role": "user", "content": current_input})
        history.append({"role": "user", "content": "**Polite AI**: "})

        polite_stream = stream_chat_api(polite_messages)
        polite_resp = ""
        if polite_stream:
            for chunk in polite_stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    polite_resp += delta.content
                    print(delta.content, end="", flush=True)
                    history[-1] = {"role": "user", "content": f"{polite_resp}"}
                    yield history
            print()

        polite_messages.append({"role": "assistant", "content": polite_resp})

        # Aggressive AI turn - streaming token by token
        aggressive_messages.append({"role": "user", "content": polite_resp})
        history.append({"role": "assistant", "content": "**Aggressive AI**: "})

        aggressive_stream = stream_chat_api(aggressive_messages)
        aggressive_resp = ""
        if aggressive_stream:
            for chunk in aggressive_stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    aggressive_resp += delta.content
                    print(delta.content, end="", flush=True)
                    history[-1] = {"role": "assistant", "content": f"{aggressive_resp}"}
                    yield history
            print()

        aggressive_messages.append({"role": "assistant", "content": aggressive_resp})

        current_input = aggressive_resp


with gr.Blocks(title="AI Agent Chat Simulation") as demo:
    gr.Markdown("# 🤖 AI Agent Chat Simulation (Polite AI vs Aggressive AI)")

    chatbot = gr.Chatbot(label="Agent Conversation", height=500)
    initial_input = gr.Textbox(value="Hi", label="Initial Prompt / Seed Message")

    with gr.Row():
        start_btn = gr.Button("Start Conversation", variant="primary")
        stop_btn = gr.Button("Stop Conversation", variant="stop")

    chat_event = start_btn.click(
        fn=simulate_chat,
        inputs=[initial_input],
        outputs=[chatbot]
    )

    stop_btn.click(fn=None, cancels=[chat_event])

if __name__ == "__main__":
    demo.launch()

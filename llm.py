import json
from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME, LLM_TEMPERATURE, MAX_TOKEN
import openai

openai.api_key = CHAT_COMPLETIONS_API_KEY
openai.base_url = API_URL


def _normalize_message(message):
    # Convert OpenAI ChatCompletionMessage objects to dicts
    if hasattr(message, 'role') and not isinstance(message, dict):
        msg = {"role": message.role, "content": message.content}
        if hasattr(message, 'tool_calls') and message.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in message.tool_calls
            ]
        return [msg]

    if isinstance(message, dict):
        role = message.get("role")
        # Tool responses and assistant messages with tool_calls: pass through as-is
        if role == "tool" or message.get("tool_calls"):
            return [message]
        content = message.get("content")
        if role is None or content is None:
            return []
        return [{"role": role, "content": content}]

    if isinstance(message, (list, tuple)) and len(message) == 2:
        user_content, assistant_content = message
        if isinstance(user_content, str) and isinstance(assistant_content, str):
            return [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
            ]

    if isinstance(message, (list, tuple)):
        sanitized = []
        for item in message:
            sanitized.extend(_normalize_message(item))
        return sanitized

    return []


def sanitize_messages(messages):
    sanitized = []
    for message in messages:
        sanitized.extend(_normalize_message(message))
    return sanitized


def call_chat_api(messages, tools=[], disable_reasoning=True, stream=False):
    """
    Calls the LLM API with tools for function calling using OpenAI library.
    Args:
        messages: List of chat messages.
        tools: Optional list of tool definitions for function calling.
        disable_reasoning: If True, sets reasoning_effort to 'none'.
        stream: If True, streams the response and returns the full content string.
                If False (default), returns the full response object.
    Returns the response object (stream=False) or content string (stream=True),
    or None on failure.
    """
    messages = sanitize_messages(messages)

    extra_body: dict = {}
    if disable_reasoning:
        extra_body["reasoning_effort"] = "none"

    try:
        print(f"\n[DEBUG] Calling LLM API with model: {LLM_MODEL_NAME} (stream={stream})")
        print(f"[DEBUG] Messages: {json.dumps(messages, indent=2)}")
        if tools:
            print(f"[DEBUG] Tools: {json.dumps(tools, indent=2)}")

        response = openai.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages,
            tools=tools,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKEN,
            extra_body=extra_body,
            stream=stream,
        )

        if stream:
            full_content = ""
            for chunk in response:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    print(delta.content, end="", flush=True)
                    full_content += delta.content
            print()  # newline after streaming output
            return full_content

        usage = getattr(response, "usage", None)
        if usage:
            print(f"[DEBUG] Usage - Tokens: {usage.total_tokens} (Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens})")

        return response
    except Exception as e:
        print(f"\n[ERROR] Error calling LLM API: {str(e)}")
        return None

def stream_chat_api(messages, disable_reasoning=True):
    messages = sanitize_messages(messages)
    extra_body: dict = {}
    if disable_reasoning:
        extra_body["reasoning_effort"] = "none"

    try:
        print(f"\n[DEBUG] Calling LLM API with model: {LLM_MODEL_NAME} (stream=True)")
        print(f"[DEBUG] Messages: {json.dumps(messages, indent=2)}")
        return openai.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKEN,
            extra_body=extra_body,
            stream=True,
        )
    except Exception as e:
        print(f"\n[ERROR] Error calling LLM API: {str(e)}")
        return None
    

#Test Run
if __name__ == "__main__":
    test_messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
    print("\n--- Testing call_chat_api ---")
    response = call_chat_api(test_messages)
    if response and response.choices:
        print("\n[RESPONSE]")
        print(response.choices[0].message.content)
    else:
        print("\n[RESPONSE] Failed to get a valid response.")
    print("-----------------------------\n")

import sys
from llm import call_chat_api

system_prompt = "generate one best suited email subject line for the email content shared"

print("Please paste the email content below. Press Ctrl+D (or Ctrl+Z on Windows) when finished:")
user_prompt = sys.stdin.read().strip()

if not user_prompt:
    print("No email content provided.")
    sys.exit(1)

# Step 2: Make the messages list
messages = [{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}]

# Step 3: Call OpenAI
response = call_chat_api(messages)

# Step 4: print the result
if response is None:
    print("\nError: Failed to get a response from the LLM.")
else:
    print("\nGenerated Subject:")
    print(response.choices[0].message.content)
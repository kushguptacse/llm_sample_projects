from llm import call_chat_api
from scraper import fetch_website_contents

system_prompt = "You are a helpful assistant that summarizes web pages."
user_prompt = """Summarize the following web page. 

"""
def fetch_webpage(web_url):
    try:
        return fetch_website_contents(web_url)
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return ""

def summarize_url(url: str) -> str:
    content = fetch_webpage(url)
    if not content:
        return "Error: Could not retrieve webpage content."
        
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": f"{user_prompt}\n\n{content}\n"}
    ]
    
    response = call_chat_api(messages)
    if response and response.choices:
        return response.choices[0].message.content
    return "Error: Failed to generate summary."

if __name__ == '__main__':
    # Test execution
    print(summarize_url("https://anthropic.com"))
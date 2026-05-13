from llm import call_chat_api
from scraper import fetch_website_contents

system_prompt = "You are a helpful assistant that summarizes web pages."
user_prompt = """Summarize the following web page. 

"""
def fetch_webpage(web_url):
    try:
        return fetch_website_contents(web_url)
    except Exception as e:
        print(e)

messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt +  "\n" + fetch_webpage("https://anthropic.com") + "\n"}]

response = call_chat_api(messages)
print(response.choices[0].message.content)
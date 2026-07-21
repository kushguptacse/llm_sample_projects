from llm import call_chat_api
from scraper import fetch_website_links

link_system_prompt = """
You are provided with a list of links found on a webpage.
You need to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(url) -> str:
    user_prompt = f"""Here is the list of links on the website {url} -
        Please decide which of these are relevant web links for a brochure about the company, 
        respond with the full https URL in JSON format.
        Do not include Terms of Service, Privacy, email links.

        Links (some might be relative links):

        """
    links  = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

def select_relevant_link_by_llm(url):
    messages = [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": get_links_user_prompt(url)}
    ]
    response = call_chat_api(messages)
    return response.choices[0].message.content

print(select_relevant_link_by_llm("https://edwarddonner.com"))
    
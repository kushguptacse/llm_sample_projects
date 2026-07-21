from llm import call_chat_api
from scraper import fetch_website_links, fetch_website_contents
import json

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
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links

def fetch_page_and_all_relevant_links(url):
    """
    Fetches and extracts text content and relevant links from a given website URL.
    """
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_link_by_llm(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result
    
brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    content_and_links = fetch_page_and_all_relevant_links(url)
    user_prompt += content_and_links
    return user_prompt

def create_brochure(company_name, url):
    messages = [
        {"role": "system", "content": brochure_system_prompt},
        {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
    ]
    call_chat_api(messages, stream=True)

# invoke create_brochure by taking company_name and url input from  command line 
if __name__ == "__main__":
    company_name = input("Enter company name: ").strip()
    url = input("Enter company website URL: ").strip()
    if not url.startswith("http"):
        url = f"https://{url}"
    create_brochure(company_name, url)
    

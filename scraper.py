import requests
from bs4 import BeautifulSoup

def fetch_website_contents(url: str) -> str:
    """
    Fetches and extracts text content from a given website URL.
    """
    try:
        # Add headers to mimic a typical browser request and prevent some sites from blocking us
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            script_or_style.extract()
            
        # Extract text
        text = soup.get_text(separator=' ')
        
        # Collapse whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

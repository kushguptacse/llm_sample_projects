# LLM Sample Projects

A collection of code snippets and sample projects demonstrating various aspects of Large Language Models (LLMs).

## 📂 Project Structure

    - `llm.py`: Core LLM client for interacting with the Qwen 3 model.
    - `config.py`: Configuration for API keys, model names, and other settings.
    - `brochure.py`: Generator script that scrapes a company website and creates a company brochure using LLM.
    - `app.py`: FastAPI web application for website summarization.
    - `email_subject_generator.py`: CLI script for generating email subject lines from body content.
    - `llm_chats.py`: Gradio app simulating a debate between polite and aggressive AI agents.
    - `scraper.py`: Web scraping utilities to fetch text content and links from websites.
    - `test_llm.py`: Test suite for validating LLM client functionality and message sanitization.
    - `web_url_summary.py`: Utility module to fetch and summarize web page contents using LLM.
    - `requirements.txt`: Dependencies for the project.

## 🚀 Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kushguptacse/llm_sample_projects.git
   cd llm_sample_projects
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

- Run `/bin/python3 test_llm.py` for llm testing example with qwen3.
- Run `python brochure.py` to generate a markdown brochure for a company by entering its name and website URL.

### LLM Notes

1. Common closed source frontier models are 
    GPT5, 
    Claude opus4.5, 
    Gemini 3 pro.

2. Common open source frontier models are 
    Qwen 3.6, 
    LLaMA 3.3, 
    Llama 4 Maverick,
    GPT-OSS,
    DeepSeek-R1

3. Models can be executed locally either by using Hugging Face models through the Transformers Python library, or via Ollama, which provides selected models optimized for local deployment.
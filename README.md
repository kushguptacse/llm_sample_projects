# LLM Sample Projects

A collection of code snippets and sample projects demonstrating various aspects of Large Language Models (LLMs).

## 📂 Project Structure

- **Week 1**:
    - `llm.py`: Core LLM client for interacting with the Qwen 3 model.
    - `config.py`: Configuration for API keys, model names, and other settings.
    - `main.py`: Example usage of the LLM client.
    - `requirements.txt`: Dependencies for the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.6+

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm_sample_projects
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run `/bin/python3 test_llm.py` for llm testing example with qwen3.

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

4. 
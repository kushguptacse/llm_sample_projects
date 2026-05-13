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

### Running the Web Application

To launch the AI Website Summarizer web interface, run the following command:

```bash
python3 app.py
```

*Alternatively, you can run it via Uvicorn directly:*
```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

Once the server starts, open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**.

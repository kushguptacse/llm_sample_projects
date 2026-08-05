
import os
from dotenv import load_dotenv

load_dotenv(override=True)
MAX_TOKEN = int(os.getenv("MAX_TOKEN", "8192"))
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME","qwen3-6-35b-a3b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
API_URL = os.getenv("API_URL","https://qwen3-spc-ap-northeast-1-a.jieum.samsungspc.cloud/v1/")
#API_URL = os.getenv("API_URL","https://playgrnd-spc-ap-northeast-1-a.jieum.samsungspc.cloud/v1/")

CHAT_COMPLETIONS_API_KEY = os.getenv("CHAT_COMPLETIONS_API_KEY")
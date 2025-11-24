# langgraph_university/config.py

import os
from dotenv import load_dotenv
from langchain_ibm import ChatWatsonx

load_dotenv()


WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
PROJECT_ID = os.getenv("PROJECT_ID")
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "meta-llama/llama-3-2-90b-vision-instruct")

if not WATSONX_URL or not WATSONX_APIKEY or not PROJECT_ID:
    raise RuntimeError("Missing one of: WATSONX_URL, WATSONX_APIKEY, PROJECT_ID")

# LLM
llm = ChatWatsonx(
    model_id=CHAT_MODEL_ID,
    url=WATSONX_URL,
    project_id=PROJECT_ID,
    params={
        "decoding_method": "sample",
        "max_new_tokens": 300,
        "temperature": 0.2,
        "top_p": 0.95,
    }
)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DEFAULT_STUDENT_ID = os.getenv("DEFAULT_STUDENT_ID", "12345")

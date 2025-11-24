import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    api_key=os.getenv("WATSONX_APIKEY"),
)

BASE_URL = os.getenv("UNIVERSITY_BACKEND_URL", "http://localhost:8000")
STUDENT_ID = "12345"  # mock fisso

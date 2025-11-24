from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="book_exam",
    description="""Book an exam for a student. 
ALWAYS answer in the same language as the user.""",
)
def book_exam(
    student_id: str = Field(..., description="Student ID"),
    exam_id: str = Field(..., description="Exam ID")
) -> str:
    try:
        r = requests.post(f"{BASE_URL}/student/{student_id}/book/{exam_id}")
        return json.dumps(r.json())
    except Exception as e:
        return f"Error booking exam: {str(e)}"

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_student_record",
    description="""Return personal and academic information about a student.
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_student_record(
    student_id: str = Field(..., description="Student ID")
) -> str:
    try:
        response = requests.get(f"{BASE_URL}/student/{student_id}")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching student record: {str(e)}"

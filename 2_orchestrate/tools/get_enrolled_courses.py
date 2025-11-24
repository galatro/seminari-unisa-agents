from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_enrolled_courses",
    description="""Return the list of courses the student is enrolled in.
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_enrolled_courses(
    student_id: str = Field(..., description="Student ID")
) -> str:
    try:
        r = requests.get(f"{BASE_URL}/student/{student_id}/courses")
        return json.dumps(r.json())
    except Exception as e:
        return f"Error: {str(e)}"

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_exam_calendar",
    description="""Return exam dates for a course.
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_exam_calendar(
    course_code: str = Field(..., description="Course code")
) -> str:
    try:
        response = requests.get(f"{BASE_URL}/campus/exams/{course_code}")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching exam calendar: {str(e)}"

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_class_schedule",
    description="""Return the schedule of a given course. 
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_class_schedule(
    course_code: str = Field(..., description="Course code, e.g. ALG-101")
) -> str:
    try:
        response = requests.get(f"{BASE_URL}/campus/schedule/{course_code}")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching schedule: {str(e)}"

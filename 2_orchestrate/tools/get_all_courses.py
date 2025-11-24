from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_all_courses",
    description="""Return a list of all university courses.
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_all_courses() -> str:
    try:
        response = requests.get(f"{BASE_URL}/campus/courses")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching courses: {str(e)}"

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="get_professor_info",
    description="""Return information about a professor (surname only).
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_professor_info(
    surname: str = Field(..., description="Professor surname, lowercase")
) -> str:
    try:
        response = requests.get(f"{BASE_URL}/campus/professor/{surname}")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching professor info: {str(e)}"


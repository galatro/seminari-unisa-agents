from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json

BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"

@tool(
    name="find_room_location",
    description="""Return the location of a room (building, floor, capacity).
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def find_room_location(
    room_code: str = Field(..., description="Room code, e.g. A1, Lab3")
) -> str:
    try:
        response = requests.get(f"{BASE_URL}/campus/room/{room_code}")
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching room location: {str(e)}"

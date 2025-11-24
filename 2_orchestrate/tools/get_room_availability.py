from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import Field
import requests, json
BASE_URL = "https://unisa-be.21ubi2trvpxv.eu-de.codeengine.appdomain.cloud"
@tool(
    name="get_room_availability",
    description="""Return all rooms available in a given date and time slot.
ALWAYS answer in the same language as the user.""",
    permission=ToolPermission.READ_ONLY,
)
def get_room_availability(
    date: str = Field(..., description="Date in YYYY-MM-DD format"),
    time_slot: str = Field(..., description="Time interval, e.g. 10:00-12:00")
) -> str:
    try:
        response = requests.get(
            f"{BASE_URL}/campus/rooms/availability",
            params={"date": date, "time_slot": time_slot}
        )
        return json.dumps(response.json())
    except Exception as e:
        return f"Error fetching room availability: {str(e)}"

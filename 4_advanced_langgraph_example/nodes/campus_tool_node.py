import json
from state import AppState
from tools import campus_tools

def campus_tool_node(state: AppState) -> AppState:

    tool_name = state.tool_name
    args = state.tool_args or {}

    TOOL_MAP = {
        "get_class_schedule": lambda: campus_tools.get_class_schedule(
            args.get("course_code", "")
        ),
        "get_room_availability": lambda: campus_tools.get_room_availability(
            args.get("date", ""), args.get("time_slot", "")
        ),
        "get_exam_calendar": lambda: campus_tools.get_exam_calendar(
            args.get("course_code", "")
        ),
        "get_professor_info": lambda: campus_tools.get_professor_info(
            args.get("surname", "")
        ),
        "find_room_location": lambda: campus_tools.find_room_location(
            args.get("room_code", "")
        ),
        "get_all_courses": lambda: campus_tools.get_all_courses(),
    }

    output = TOOL_MAP.get(tool_name, lambda: {"error": "tool sconosciuto"})()

    # salva tutto nello state
    state.tool_output = output

    # context sempre come lista di stringhe
    if isinstance(output, list):
        state.context = [json.dumps(o, ensure_ascii=False) for o in output]
    else:
        state.context = [json.dumps(output, ensure_ascii=False)]

    return state

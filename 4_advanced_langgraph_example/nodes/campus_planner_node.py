import json
from state import AppState
from config import llm

def campus_planner_node(state: AppState) -> AppState:
    query = state.input_text

    PROMPT = """
Sei un agente che deve scegliere il tool corretto per informazioni sul CAMPUS.

Tool disponibili:
1) get_class_schedule        -> {{"course_code": "ALG-101"}}
2) get_room_availability     -> {{"date": "YYYY-MM-DD", "time_slot": "HH:MM-HH:MM"}}
3) get_exam_calendar         -> {{"course_code": "ALG-101"}}
4) get_professor_info        -> {{"surname": "Rossi"}}
5) find_room_location        -> {{"room_code": "A-12"}}
6) get_all_courses           -> {{}}

Rispondi SOLO con JSON: {{"tool": "nome", "arguments": {{"argument": "{{value}}", ...}}}}


Domanda: \"\"\"{query}\"\"\"
"""

    raw = llm.invoke(PROMPT.format(query=query)).content

    try:
        first = raw.find("{")
        last = raw.rfind("}")
        plan = json.loads(raw[first:last+1])
    except:
        plan = {"tool": "get_all_courses", "arguments": {}}

    state.tool_name = plan.get("tool", "get_all_courses")
    state.tool_args = plan.get("arguments", {})

    return state

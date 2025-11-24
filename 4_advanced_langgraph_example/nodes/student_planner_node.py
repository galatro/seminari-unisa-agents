import json
from typing import Dict, Any
from state import AppState
from config import llm


def student_planner_node(state: AppState) -> dict:
    """
    Planner: sceglie il tool corretto in base alla domanda.
    Non esegue il tool, decide solo nome + argomenti.
    """
    query = state.input_text
    student_id = state.student_id or "12345"

    PLANNING_PROMPT = """
Sei un agente che deve scegliere il tool corretto per il RECORD PERSONALE dello studente.

STUDENT ID: {student_id}

Tool disponibili:
1) get_student_record, 2) get_completed_exams, 3) get_available_exams
4) get_enrolled_courses, 5) get_gpa, 6) book_exam (richiede exam_id)
7) get_booked_exams, 8) get_next_exams

Rispondi SOLO con JSON: {{"tool": "nome", "arguments": {{"student_id": "{student_id}", ...}}}}

Domanda: \"\"\"{query}\"\"\"
"""

    raw_plan = llm.invoke(
        PLANNING_PROMPT.format(query=query, student_id=student_id)
    ).content

    try:
        first = raw_plan.find("{")
        last = raw_plan.rfind("}")
        plan = json.loads(raw_plan[first:last + 1])
    except Exception:
        plan = {"tool": "get_gpa", "arguments": {"student_id": student_id}}

    tool_name: str = plan.get("tool", "get_gpa")
    tool_args: Dict[str, Any] = plan.get("arguments", {}) or {}
    tool_args["student_id"] = student_id

    return {
        "selected_tool_name": tool_name,
        "selected_tool_args": tool_args,
        "student_id": student_id,
        "agent_domain": "student",
    }

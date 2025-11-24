import json
import uuid
from typing import Dict, Any
from state import AppState
from tools import student_tools


AVAILABLE_TOOLS = {
    "get_student_record": lambda sid, args: student_tools.get_student_record(sid),
    "get_completed_exams": lambda sid, args: student_tools.get_completed_exams(sid),
    "get_available_exams": lambda sid, args: student_tools.get_available_exams(sid),
    "get_enrolled_courses": lambda sid, args: student_tools.get_enrolled_courses(sid),
    "get_gpa": lambda sid, args: student_tools.get_gpa(sid),
    "book_exam": lambda sid, args: student_tools.book_exam(sid, args.get("exam_id", "")),
    "get_booked_exams": lambda sid, args: student_tools.get_booked_exams(sid),
    "get_next_exams": lambda sid, args: student_tools.get_next_exams(sid),
}


def student_tool_node(state: AppState) -> dict:
    """
    Esegue il tool selezionato dal planner e costruisce il contesto.
    """
    student_id = state.student_id or "12345"
    tool_name = state.selected_tool_name or "get_gpa"
    tool_args: Dict[str, Any] = dict(state.selected_tool_args or {})
    tool_args["student_id"] = student_id

    tool_fn = AVAILABLE_TOOLS.get(
        tool_name,
        lambda sid, args: {"error": "Tool sconosciuto", "tool_name": tool_name},
    )

    tool_output = tool_fn(student_id, tool_args)

    if isinstance(tool_output, list):
        context_list = [json.dumps(item, ensure_ascii=False) for item in tool_output]
    else:
        context_list = [json.dumps(tool_output, ensure_ascii=False)]

    tool_call_record = [
        {
            "id": str(uuid.uuid4()),
            "name": tool_name,
            "args": tool_args,
        }
    ]

    return {
        "tool_name": tool_name,
        "tool_args": tool_args,
        "tool_output": tool_output,
        "tool_calls": tool_call_record,
        "context": context_list,
        "agent_domain": "student",
    }

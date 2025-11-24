# student_agent_node.py
import json
from typing import Dict, Any
import uuid

from state import AppState
from config import llm
from tools import student_tools


def student_agent_node(state: AppState):
    """Nodo terminale del dominio STUDENTE."""
    
    query = state.input_text
    student_id = state.student_id or "12345"

    # --------------------------------------------------------
    # 1) PLANNING
    # --------------------------------------------------------
    PLANNING_PROMPT = """
Sei un agente che deve scegliere il tool corretto per il RECORD PERSONALE dello studente.

STUDENT ID: {student_id}

Tool disponibili:
1) get_student_record, 2) get_completed_exams, 3) get_available_exams
4) get_enrolled_courses, 5) get_gpa, 6) book_exam (richiede exam_id)
7) get_booked_exams, 8) get_next_exams

Rispondi SOLO con JSON: {{"tool": "nome", "arguments": {{"student_id": "{student_id}"}}}}

Domanda: \"\"\"{query}\"\"\"
"""

    raw_plan = llm.invoke(PLANNING_PROMPT.format(query=query, student_id=student_id)).content

    try:
        first = raw_plan.find("{")
        last = raw_plan.rfind("}")
        plan = json.loads(raw_plan[first:last+1])
    except Exception:
        plan = {"tool": "get_gpa", "arguments": {"student_id": student_id}}

    tool_name: str = plan.get("tool", "get_gpa")
    tool_args: Dict[str, Any] = plan.get("arguments", {})
    tool_args["student_id"] = student_id

    # --------------------------------------------------------
    # 2) EXECUTION
    # --------------------------------------------------------
    tool_map = {
        "get_student_record": lambda: student_tools.get_student_record(tool_args["student_id"]),
        "get_completed_exams": lambda: student_tools.get_completed_exams(tool_args["student_id"]),
        "get_available_exams": lambda: student_tools.get_available_exams(tool_args["student_id"]),
        "get_enrolled_courses": lambda: student_tools.get_enrolled_courses(tool_args["student_id"]),
        "get_gpa": lambda: student_tools.get_gpa(tool_args["student_id"]),
        "book_exam": lambda: student_tools.book_exam(tool_args["student_id"], tool_args.get("exam_id", "")),
        "get_booked_exams": lambda: student_tools.get_booked_exams(tool_args["student_id"]),
        "get_next_exams": lambda: student_tools.get_next_exams(tool_args["student_id"]),
    }
    
    tool_output = tool_map.get(tool_name, lambda: {"error": "Tool sconosciuto"})()

    if isinstance(tool_output, list):
        context_list = [json.dumps(item, ensure_ascii=False) for item in tool_output]
    else:
        context_list = [json.dumps(tool_output, ensure_ascii=False)]

    # --------------------------------------------------------
    # 3) FINAL ANSWER
    # --------------------------------------------------------
    ANSWER_PROMPT = """
Sei l'assistente universitario per il RECORD PERSONALE dello studente.

Domanda: \"\"\"{query}\"\"\"
Informazioni dal sistema: {context}

Genera una risposta CHIARA, IN ITALIANO, utile e completa.
Non menzionare tool o API.
"""

    final_answer = llm.invoke(
        ANSWER_PROMPT.format(query=query, context="\n".join(context_list))
    ).content.strip()

    return {
        "context": context_list,
        "generated_text": final_answer,

        # campi richiesti dal valutatore
        "tool_name": tool_name,
        "tool_args": tool_args,
        "tool_output": tool_output,
        "tool_calls": [
            {
                "id": str(uuid.uuid4()),
                "name": tool_name,
                "args": tool_args
            }
        ],
        "domain": "student",
    }

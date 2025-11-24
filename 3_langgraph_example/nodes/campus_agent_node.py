# campus_agent_node.py
import json
from typing import Dict, Any
import uuid
from state import AppState
from config import llm
from tools import campus_tools


def campus_agent_node(state: AppState):
    """Nodo terminale del dominio CAMPUS."""
    
    query = state.input_text

    # --------------------------------------------------------
    # 1) PLANNING
    # --------------------------------------------------------
    PLANNING_PROMPT = """
Sei un agente che deve scegliere il tool corretto per rispondere a domande 
sulle informazioni di CAMPUS universitario.

Tool disponibili:
1) "get_class_schedule" - parametri: {{"course_code": "ALG-101"}}
2) "get_room_availability" - parametri: {{"date": "YYYY-MM-DD", "time_slot": "HH:MM-HH:MM"}}
3) "get_exam_calendar" - parametri: {{"course_code": "<codice>"}}
4) "get_professor_info" - parametri: {{"surname": "<cognome prof>"}}
5) "find_room_location" - parametri: {{"room_code": "<codice aula>"}}
6) "get_all_courses" - parametri: {{}}

Rispondi SOLO con JSON: {{"tool": "nome", "arguments": {{}}}}

Domanda: \"\"\"{query}\"\"\"
"""

    raw_plan = llm.invoke(PLANNING_PROMPT.format(query=query)).content
    
    try:
        first = raw_plan.find("{")
        last = raw_plan.rfind("}")
        plan = json.loads(raw_plan[first:last+1])
    except Exception:
        plan = {"tool": "get_all_courses", "arguments": {}}

    tool_name: str = plan.get("tool", "get_all_courses")
    tool_args: Dict[str, Any] = plan.get("arguments", {})

    # --------------------------------------------------------
    # 2) EXECUTION
    # --------------------------------------------------------
    if tool_name == "get_class_schedule":
        tool_output = campus_tools.get_class_schedule(tool_args.get("course_code", ""))
    elif tool_name == "get_room_availability":
        tool_output = campus_tools.get_room_availability(
            tool_args.get("date", ""), tool_args.get("time_slot", "")
        )
    elif tool_name == "get_exam_calendar":
        tool_output = campus_tools.get_exam_calendar(tool_args.get("course_code", ""))
    elif tool_name == "get_professor_info":
        tool_output = campus_tools.get_professor_info(tool_args.get("surname", ""))
    elif tool_name == "find_room_location":
        tool_output = campus_tools.find_room_location(tool_args.get("room_code", ""))
    else:
        tool_output = campus_tools.get_all_courses()

    if isinstance(tool_output, list):
        context_list = [json.dumps(item, ensure_ascii=False) for item in tool_output]
    else:
        context_list = [json.dumps(tool_output, ensure_ascii=False)]

    # --------------------------------------------------------
    # 3) FINAL ANSWER
    # --------------------------------------------------------
    ANSWER_PROMPT = """
Sei l'assistente universitario specializzato in informazioni di CAMPUS.

Domanda: \"\"\"{query}\"\"\"
Informazioni disponibili: {context}

Genera una risposta CHIARA, IN ITALIANO, utile e sintetica.
Non nominare il "tool" né dettagli tecnici.
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
        "domain": "campus",
    }
    
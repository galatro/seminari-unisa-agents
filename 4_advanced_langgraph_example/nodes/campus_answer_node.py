import uuid
from state import AppState
from config import llm, evaluator, llm_judge
from ibm_watsonx_gov.evaluators.agentic_evaluator import AgenticAIConfiguration
from ibm_watsonx_gov.metrics import ToolCallParameterAccuracyMetric
from tools.campus_tools import *

AVAILABLE_TOOLS = [
    get_class_schedule,
    get_room_availability,
    get_exam_calendar,
    get_professor_info,
    find_room_location,
    get_all_courses,
]

agentic_config = AgenticAIConfiguration(tools=AVAILABLE_TOOLS)


@evaluator.evaluate_tool_call_accuracy(configuration=agentic_config)
@evaluator.evaluate_tool_call_parameter_accuracy(
    configuration=agentic_config,
    metrics=[ToolCallParameterAccuracyMetric(llm_judge=llm_judge)]
)
@evaluator.evaluate_context_relevance()
@evaluator.evaluate_faithfulness()
@evaluator.evaluate_answer_relevance()
def campus_answer_node(state: AppState):

    query = state.input_text
    context = "\n".join(state.context or [])

    ANSWER_PROMPT = """
Sei l’assistente universitario del CAMPUS.

Domanda: \"\"\"{query}\"\"\"
Informazioni dal sistema:
{context}

Rispondi in modo chiaro, utile e sintetico.
"""

    final_answer = llm.invoke(
        ANSWER_PROMPT.format(query=query, context=context)
    ).content.strip()

    return {
        "generated_text": final_answer,
        "context": state.context,
        "tool_name": state.tool_name,
        "tool_args": state.tool_args,
        "tool_output": state.tool_output,
        "tool_calls": [
            {
                "id": str(uuid.uuid4()),
                "name": state.tool_name,
                "args": state.tool_args,
            }
        ],
        "domain": "campus",
    }

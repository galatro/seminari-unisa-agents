import uuid
from state import AppState
from config import llm, evaluator, llm_judge
from ibm_watsonx_gov.evaluators.agentic_evaluator import AgenticAIConfiguration
from ibm_watsonx_gov.metrics import ToolCallParameterAccuracyMetric
from tools import student_tools

AVAILABLE_TOOLS = [
    student_tools.get_student_record,
    student_tools.get_completed_exams,
    student_tools.get_available_exams,
    student_tools.get_enrolled_courses,
    student_tools.get_gpa,
    student_tools.book_exam,
    student_tools.get_booked_exams,
    student_tools.get_next_exams,
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
def student_answer_node(state: AppState):

    query = state.input_text
    context = "\n".join(state.context)

    ANSWER_PROMPT = """
Sei l’assistente universitario per il RECORD PERSONALE dello studente.

Domanda: \"\"\"{query}\"\"\"
Informazioni dal sistema:
{ctx}

Rispondi in modo chiaro e utile.
"""

    answer = llm.invoke(
        ANSWER_PROMPT.format(query=query, ctx=context)
    ).content.strip()

    return {
        "generated_text": answer,
        "context": state.context,
        "tool_name": state.tool_name,
        "tool_args": state.tool_args,
        "tool_output": state.tool_output,
        "tool_calls": state.tool_calls,
        "domain": "student",
    }

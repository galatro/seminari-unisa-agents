import asyncio
import json
import uuid
from dotenv import load_dotenv
from beeai_framework.backend import ChatModel, UserMessage
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.tools import tool, StringToolOutput
from beeai_framework.memory import UnconstrainedMemory
from langgraph.graph import StateGraph, START, END
from ibm_watsonx_gov.evaluators.agentic_evaluator import AgenticEvaluator
from ibm_watsonx_gov.entities.state import EvaluationState


load_dotenv()

@tool
def get_gpa(student_id: str) -> StringToolOutput:
    """
    Restituisce la media (GPA) di uno studente.

    Args:
        student_id (str): ID dello studente.

    Returns:
        StringToolOutput: JSON {"student_id": ..., "gpa": ...}
    """
    return StringToolOutput(json.dumps({"student_id": student_id, "gpa": 27.3}))


@tool
def get_class_schedule(course_code: str) -> StringToolOutput:
    """
    Restituisce gli orari di un corso universitario.

    Args:
        course_code (str): Codice del corso.

    Returns:
        StringToolOutput: JSON {"course": ..., "slots": [...]}
    """
    return StringToolOutput(json.dumps({
        "course": course_code,
        "slots": ["Mon 10-12", "Wed 14-16"]
    }))

llm = ChatModel.from_name("watsonx:meta-llama/llama-3-2-90b-vision-instruct")

bee_agent = RequirementAgent(
    name="UniversityAgent",
    llm=llm,
    tools=[get_gpa, get_class_schedule],
    memory=UnconstrainedMemory(),
    instructions="""
Se l’utente chiede il GPA → usa get_gpa.
Se chiede orari di un corso → usa get_class_schedule.
Rispondi sempre in italiano.
"""
)

async def call_bee_async(question: str) -> str:
    run = bee_agent.run([UserMessage(question)])
    out = await run
    return out.last_message.text

def call_bee_sync(question: str) -> str:
    return asyncio.run(call_bee_async(question))

class MyState(EvaluationState):
    input_text: str = ""
    generated_text: str = ""

    context: list = []
    ground_truth: str = ""
    tool_calls: list = []
    available_tools: list = []
    model_prompt: str = ""


evaluator = AgenticEvaluator()

graph = StateGraph(MyState)

@evaluator.evaluate_faithfulness()
def bee_agent_node(state: MyState) -> dict:
    """
    Nodo LangGraph che incapsula l'agente Bee.
    Il decorator raccoglie le metriche dal dict ritornato.
    """

    answer = call_bee_sync(state.input_text)

    return {
        "generated_text": answer,
        "context": [],                      # richiesto
        "tool_calls": [],                   # Bee non li esporta
        "available_tools": ["get_gpa", "get_class_schedule"],
        "model_prompt": "",                 # opzionale
        "ground_truth": "",                 # reference-free ok
        # campi minimi richiesti per le metriche governative:
        "input_text": state.input_text,     # serve al decorator
        "interaction_id": state.interaction_id
    }



graph.add_node("bee_agent_node", bee_agent_node)
graph.add_edge(START, "bee_agent_node")
graph.add_edge("bee_agent_node", END)

app = graph.compile()


if __name__ == "__main__":
    evaluator.start_run()

    state = MyState(
        interaction_id=str(uuid.uuid4()),
        input_text="Qual è la mia media?"
    )

    final_state = app.invoke(state)

    evaluator.end_run()

    print("\n=== RISPOSTA DELL'AGENTE ===")
    print(final_state.get('generated_text'))

    print("\n=== RISULTATI METRICHE ===")
    print(evaluator.get_result())

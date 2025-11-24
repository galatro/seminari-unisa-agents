from typing import Any, Dict, List, Optional
from ibm_watsonx_gov.entities.state import EvaluationState


class AppState(EvaluationState):
    """
    Stato condiviso nel grafo LangGraph.
    Estende EvaluationState così i valutatori IBM trovano
    i campi che si aspettano (message_id, etc).
    """

    # Input base
    input_text: str
    student_id: Optional[str] = None
    interaction_id: Optional[str] = None

    # Routing
    domain: Optional[str] = None  # "student" / "campus"

    # Pianificazione tools (planner)
    selected_tool_name: Optional[str] = None
    selected_tool_args: Optional[Dict[str, Any]] = None

    # Output tools (executor)
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

    # Contesto per la risposta
    context: Optional[List[str]] = None

    # Risposta finale
    generated_text: Optional[str] = None

    # Dominio dell’agente (per i valutatori)
    agent_domain: Optional[str] = None

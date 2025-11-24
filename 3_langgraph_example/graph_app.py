from langgraph.graph import StateGraph, START, END

from state import AppState
from nodes.router_node import RouterNode
from nodes.campus_agent_node import campus_agent_node
from nodes.student_agent_node import student_agent_node


def _route_by_domain(state: AppState) -> str:
    """
    Funzione di routing per le conditional edges:
    legge state.domain impostato dal RouterNode.

    Deve restituire una chiave tra quelle del dict passato a add_conditional_edges.
    """
    if state.domain == "student":
        return "student_agent"
    # default conservativo
    return "campus_agent"


def build_graph():
    """
    Costruisce e compila il grafo LangGraph per l'assistente universitario.
    Ritorna l'oggetto 'app' che puoi usare con .invoke() o .batch().
    """
    graph = StateGraph(AppState)

    # Nodi
    router = RouterNode()
    graph.add_node("router", router)
    graph.add_node("campus_agent", campus_agent_node)
    graph.add_node("student_agent", student_agent_node)

    # Entry point
    graph.add_edge(START, "router")

    # Dopo il router, scegli in base a state.domain
    graph.add_conditional_edges(
        "router",
        _route_by_domain,
        {
            "campus_agent": "campus_agent",
            "student_agent": "student_agent",
        },
    )

    # Nodi terminali
    graph.add_edge("campus_agent", END)
    graph.add_edge("student_agent", END)

    # Compila il grafo
    app = graph.compile()
    return app

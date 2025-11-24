from langgraph.graph import StateGraph, START, END
from state import AppState
from nodes.router_node import RouterNode
from nodes.student_planner_node import student_planner_node
from nodes.student_tool_node import student_tool_node
from nodes.student_answer_node import student_answer_node
from nodes.campus_planner_node import campus_planner_node
from nodes.campus_tool_node import campus_tool_node
from nodes.campus_answer_node import campus_answer_node
from nodes.unknown_answer_node import unknown_answer_node

def build_graph():

    graph = StateGraph(AppState)

    graph.add_node("router", RouterNode())

    # STUDENTE
    graph.add_node("student_planner", student_planner_node)
    graph.add_node("student_tools", student_tool_node)
    graph.add_node("student_answer", student_answer_node)

    # CAMPUS
    graph.add_node("campus_planner", campus_planner_node)
    graph.add_node("campus_tools", campus_tool_node)
    graph.add_node("campus_answer", campus_answer_node)

    # UNKNOWN
    graph.add_node("unknown_answer", unknown_answer_node)

    graph.add_edge(START, "router")

    def route_domain(state: AppState):
        return state.domain  # "student", "campus", "unknown"

    graph.add_conditional_edges(
        "router",
        route_domain,
        {
            "student": "student_planner",
            "campus": "campus_planner",
            "unknown": "unknown_answer",
        },
    )

    # Flusso STUDENTE
    graph.add_edge("student_planner", "student_tools")
    graph.add_edge("student_tools", "student_answer")
    graph.add_edge("student_answer", END)

    # Flusso CAMPUS
    graph.add_edge("campus_planner", "campus_tools")
    graph.add_edge("campus_tools", "campus_answer")
    graph.add_edge("campus_answer", END)

    # Flusso UNKNOWN
    graph.add_edge("unknown_answer", END)

    return graph.compile()

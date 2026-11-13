from langgraph.graph import END, START, StateGraph

from src.graph.nodes.confirmar import confirmar
from src.graph.nodes.escalar import escalar
from src.graph.nodes.executar import executar
from src.graph.nodes.ler_estado import ler_estado
from src.graph.nodes.navegador import navegador
from src.graph.nodes.revisor import revisor
from src.graph.nodes.validar import validar
from src.graph.routing import route_after_execute, route_after_review, route_after_validate
from src.graph.state import State


def build_graph():
    graph = StateGraph(State)
    graph.add_node("ler_estado", ler_estado)
    graph.add_node("navegador", navegador)
    graph.add_node("revisor", revisor)
    graph.add_node("validar", validar)
    graph.add_node("executar", executar)
    graph.add_node("confirmar", confirmar)
    graph.add_node("escalar", escalar)

    graph.add_edge(START, "ler_estado")
    graph.add_edge("ler_estado", "navegador")
    graph.add_edge("navegador", "revisor")
    graph.add_conditional_edges(
        "revisor",
        route_after_review,
        {"aprovado": "validar", "tentar_de_novo": "navegador", "esgotado": "escalar"},
    )
    graph.add_conditional_edges(
        "validar", route_after_validate, {"executar": "executar", END: END}
    )
    graph.add_conditional_edges(
        "executar", route_after_execute, {"reler": "ler_estado", "confirmar": "confirmar"}
    )
    graph.add_edge("confirmar", END)
    graph.add_edge("escalar", END)
    return graph.compile()

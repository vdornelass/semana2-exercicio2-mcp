from langgraph.graph import END

from src.graph.state import State

MAX_RODADAS = 2
MAX_TENTATIVAS = 2


def route_after_review(state: State) -> str:
    if state["revisao"]["aprovado"]:
        return "aprovado"

    return "tentar_de_novo" if state["rodada"] < MAX_RODADAS else "esgotado"


def route_after_validate(state: State) -> str:
    return "executar" if state["valido"] else END


def route_after_execute(state: State) -> str:
    erro = state["resposta_mcp"].get("error")
    
    if erro and erro["code"] == "STATE_VERSION_CONFLICT" and state["tentativas"] < MAX_TENTATIVAS:
        return "reler"

    return "confirmar"

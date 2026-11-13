from src.graph.state import State


def confirmar(state: State) -> dict:
    r, navio = state["resposta_mcp"], state["navio"]

    if "error" in r:
        return {"resultado": f"{navio['id']}: falha {r['error']['code']} ({r['error']['message']})"}
        
    return {
        "resultado": f"{navio['id']}: velocidade ajustada de {r['before']} para {r['after']} nós "
        f"(state_version {r['state_version']})"
    }


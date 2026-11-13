from src.graph.state import State


def escalar(state: State) -> dict:
    return {
        "resultado": f"{state['navio']['id']}: sem acordo após {state['rodada']} rodadas. "
        "Escalar para o operador (nenhum comando enviado)."
    }


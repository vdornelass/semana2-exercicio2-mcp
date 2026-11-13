from src.graph.state import State


def validar(state: State) -> dict:
    proposta = state["proposta"]
    navio = state["navio"]
    velocidade = proposta["velocidade_kn"]

    if proposta["acao"] == "NO_ACTION":
        return {"valido": False, "resultado": f"{navio["id"]} nenhuma ação necessária."}

    erro = {"valido": False, "resultado": f"{navio['id']}: proposta bloqueada pela validação em código."}

    if velocidade is None or velocidade < 0 or velocidade > 18 or velocidade % 0.5 != 0:
        return erro

    if navio["em_tempestade"]:
        if navio["rota"] == "direta" and velocidade > 12:
            return erro
        
        if navio["rota"] == "protegida" and velocidade > 15:
            return erro

    return {"valido": True}
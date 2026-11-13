import os

from src.graph.state import State
from src.utils.mcp_client import get_tools_by_name, parse_result


async def executar(state: State) -> dict:
    navio = state["navio"]
    proposta = state["proposta"]
    tentativas = state.get("tentativas", 0)

    versao = navio["state_version"]
    chave = f"treino:{navio['id']}:SET_SPEED:v{versao}"

    if os.getenv("SIMULAR_CONFLITO") and tentativas == 0:
        versao -= 1

    tools = await get_tools_by_name()

    raw = await tools["set_speed"].ainvoke({
        "ship_id": navio["id"],
        "speed_kn": proposta["velocidade_kn"],
        "expected_state_version": versao,
        "idempotency_key": chave
    })

    return {
        "resposta_mcp": parse_result(raw),
        "tentativas": tentativas + 1
    }

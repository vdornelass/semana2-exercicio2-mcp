import json
from pathlib import Path

from fastmcp import FastMCP


DADOS = Path(__file__).resolve().parent.parent / "data" / "situacao_tempestade.json"
FROTA = {
    navio["id"]: navio
    for navio in json.loads(DADOS.read_text(encoding="utf-8"))["navios"]
}

mcp = FastMCP("ocean")

RESPOSTAS: dict[str, dict] = {}


def _erro(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


@mcp.tool()
def get_fleet_state() -> dict:
    """Snapshot dos navios, incluindo state_version."""

    return {"navios": list(FROTA.values())}


@mcp.tool()
def set_speed(
    ship_id: str,
    speed_kn: float,
    expected_state_version: int,
    idempotency_key: str,
) -> dict:
    """Define a velocidade-alvo (0 a 18 nós, passo 0,5). Mutável e idempotente."""
    
    if idempotency_key in RESPOSTAS:
        return {**RESPOSTAS[idempotency_key], "duplicate": True}

    navio = FROTA.get(ship_id)

    if navio is None or speed_kn < 0 or speed_kn > 18 or (speed_kn * 2) % 1 != 0:
        return _erro("INVALID_SCHEMA", "navio inexistente ou velocidade inválida")

    if navio["state_version"] != expected_state_version:
        return _erro("STATE_VERSION_CONFLICT", "versão do estado desatualizada")
    
    antes = navio["velocidade_alvo_kn"]

    navio["velocidade_alvo_kn"] = speed_kn
    navio["state_version"] += 1

    resposta = {
        "status": "committed",
        "ship_id": ship_id,
        "before": antes,
        "after": speed_kn,
        "state_version": navio["state_version"],
        "duplicate": False
    }

    RESPOSTAS[idempotency_key] = resposta

    return resposta


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

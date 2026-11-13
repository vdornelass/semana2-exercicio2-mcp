from typing import TypedDict


class State(TypedDict, total=False):
    ship_id: str
    navio: dict
    proposta: dict
    revisao: dict
    rodada: int
    valido: bool
    resposta_mcp: dict
    tentativas: int
    resultado: str
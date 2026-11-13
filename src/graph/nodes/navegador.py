import json
from typing import Literal

from pydantic import BaseModel

from src.graph.prompt.navegador_prompt import NAVEGADOR_PROMPT
from src.graph.state import State
from src.utils.llmadapter import get_llm


class Proposta(BaseModel):
    acao: Literal["SET_SPEED", "NO_ACTION"]
    velocidade_kn: float | None = None
    motivo: str


def navegador(state: State) -> dict:
    revisao = state.get("revisao", {})

    if state.get("revisao"):
        revisao = state["revisao"]
    else:
        revisao = {}
    
    if revisao.get("aprovado", True):
        feedback = ""
    else:
        feedback = revisao.get("motivo", "")
    
    chain = NAVEGADOR_PROMPT | get_llm().with_structured_output(Proposta)

    proposta = chain.invoke({
        "navio": json.dumps(state["navio"], ensure_ascii=False),
        "feedback": feedback
    })

    return {
        "proposta": proposta.model_dump(),
        "rodada": state.get("rodada", 0) + 1
    }
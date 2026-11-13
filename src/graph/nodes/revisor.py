import json

from pydantic import BaseModel

from src.graph.prompt.revisor_prompt import REVISOR_PROMPT
from src.graph.state import State
from src.utils.llmadapter import get_llm


class Revisao(BaseModel):
    aprovado: bool
    motivo: str


def revisor(state: State) -> dict:
    p = state["proposta"]

    chain = REVISOR_PROMPT | get_llm().with_structured_output(Revisao)

    revisao = chain.invoke({
        "navio": json.dumps(state["navio"], ensure_ascii=False),
        "proposta": json.dumps({
            "acao": p["acao"],
            "velocidade_kn": p["velocidade_kn"]
        })
    })

    return {"revisao": revisao.model_dump()}
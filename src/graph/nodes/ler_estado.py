from src.graph.state import State
from src.utils.mcp_client import get_tools_by_name, parse_result


async def ler_estado(state: State) -> dict:
    tools = await get_tools_by_name()
    
    frota = parse_result(await 
    tools["get_fleet_state"].ainvoke({}))["navios"]
    
    for n in frota:
        if n["id"] == state["ship_id"]:
            navio = n
            break

    return {
        "navio": navio,
        "rodada": 0,
        "revisao": {}
    }

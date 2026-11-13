import asyncio

from src.graph.builder import build_graph


async def main() -> None:
    graph = build_graph()

    for ship_id in ["S1-FAROL", "S2-MARE", "S3-CORAL"]:
        saida = await graph.ainvoke({"ship_id": ship_id})
        
        print(saida["resultado"])


if __name__ == "__main__":
    asyncio.run(main())

import json
import os

from langchain.mcp import MCPAdapter

MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")

_tools: dict | None = None


async def get_tools_by_name() -> dict:
    global _tools
    
    if _tools is None:
        async with MCPAdapter(MCP_URL) as adapter:
            _tools = {t.name: t for t in await adapter.list_tools()}
            
    return _tools


def parse_result(raw) -> dict:
    if isinstance(raw, dict):
        return raw

    if isinstance(raw, list):
        bloco = raw[0]
        raw = bloco["text"] if isinstance(bloco, dict) else bloco

    return json.loads(raw)

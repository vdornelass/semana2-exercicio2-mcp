import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


@lru_cache(maxsize=1)
def get_llm() -> AzureChatOpenAI:
    """Retorna a instância configurada do AzureChatOpenAI."""
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not api_key or not endpoint:
        raise RuntimeError("Credenciais do Azure OpenAI não configuradas no .env")

    return AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

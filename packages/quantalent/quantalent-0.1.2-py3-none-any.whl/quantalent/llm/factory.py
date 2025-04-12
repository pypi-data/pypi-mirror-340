from .openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider
from .base import LLMProvider

def get_provider(provider_name: str, **kwargs) -> LLMProvider:
    if provider_name == "openai":
        return OpenAIProvider(**kwargs)
    elif provider_name == "ollama":
        return OllamaProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
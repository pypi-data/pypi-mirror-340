from .brave_provider import BraveSearchProvider
from .base import SearchProvider


def get_provider(provider_name: str, **kwargs) -> SearchProvider:
    if provider_name == "brave":
        return BraveSearchProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
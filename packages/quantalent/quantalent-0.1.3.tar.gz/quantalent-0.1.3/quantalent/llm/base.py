from abc import ABC, abstractmethod

class LLMProvider(ABC):
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        pass

    @abstractmethod
    def summarize_url(self, url: str, **kwargs):
        pass
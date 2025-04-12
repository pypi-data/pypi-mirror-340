from typing import Optional
from quantalent.utils import scrape_url
from quantalent.llm.base import LLMProvider
import requests

class OllamaProvider(LLMProvider):

    def __init__(self, model_name: Optional[str] = "llama3.2"):
        super().__init__(model_name)
        self.OLLAMA_API = "http://localhost:11434/api/chat"
        self.HEADERS = {"Content-Type": "application/json"}

    def _payload_for(self, model, scrape_result):
        def messages_for(user_message):
            system_prompt = """
            Please summarize web page.
            Paragraphs from the web content will be provided by user.
            """
            # message = f"""
            # Please summarize this web page.
            # Paragraphs from the web content:
            # {user_message}
            #
            # """
            return [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": scrape_result}
            ]

        payload = {
            "model": model,
            "messages": messages_for(scrape_result),
            "stream": False
        }

        return payload

    def summarize_url(self, url: str, **kwargs):
        try:
            scrape_result = scrape_url(url)

            summarize_result = requests.post(
                url=self.OLLAMA_API,
                json=self._payload_for(self.model_name, scrape_result)
            )

            return summarize_result.json()["message"]["content"].strip()

        except Exception as e:
            return f"Error with OllamaProvider API: {e}"

    def ask_with_context(self, context, message):

        def messages_for(context, follow_up_question):
            system_prompt = """
            You are a useful assistant.
            This is additional context you may use when answering user's ask.
            Context: {context}
            """
            return [{"role": "system", "content": system_prompt},
                        {"role": "user", "content": follow_up_question}]

        payload = {
            "model": self.model_name,
            "messages": messages_for(context, message),
            "stream": False
        }

        llm_response = requests.post(url=self.OLLAMA_API, json=payload, headers=self.HEADERS)

        return llm_response.json()["message"]["content"]


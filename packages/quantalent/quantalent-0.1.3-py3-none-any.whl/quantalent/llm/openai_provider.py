from typing import Optional
from openai import OpenAI
from quantalent.utils import scrape_url
from quantalent.llm.base import LLMProvider
import os


class OpenAIProvider(LLMProvider):

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None, *args, **kwargs):
        super().__init__(model_name)

        # If no api_key is passed, try to get it from the environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for OpenAI model.")

        # Create openai object
        self.openai = OpenAI(api_key=self.api_key, *args, **kwargs)

    def summarize_url(self, url: str, **kwargs):

        try:
            scrape_result = scrape_url(url)

            message = f"""
            Please summarize this web page.
            Paragraphs from the web content:
            {scrape_result}

            """
            summarize_result = self.openai.chat.completions.create(
                model = self.model_name,
                messages = [{"role": "user", "content": message}],
                **kwargs
            )
            return summarize_result.choices[0].message.content.strip()

        except Exception as e:
            return f"Error with OpenAIProvider API: {e}"



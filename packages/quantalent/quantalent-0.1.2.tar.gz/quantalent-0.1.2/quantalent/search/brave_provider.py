from typing import List, Dict, Optional
from brave_search_python_client import BraveSearch, WebSearchRequest, NewsSearchRequest
from brave_search_python_client.responses.news_search import NewsResult
from quantalent.search.base import SearchProvider
import os


class BraveSearchProvider(SearchProvider):

    def __init__(self, api_key: Optional[str] = None, *args, **kwargs):

        # If no api_key is passed, try to get it from the environment
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for Brave Search API.")

        self.bs = BraveSearch(api_key=self.api_key, *args, **kwargs)

    async def search_news(self, query, count=1) -> List[NewsResult]:
        request = NewsSearchRequest(q=query, count=count)
        response = await self.bs.news(request)
        return response.results

    async def search_web(self, query, count=1) -> List[Dict[str, str]]:
        """
        Searches using Brave Search API with a given query and API key.

        Args:
            query (str): The search query.
            api_key (str): The API key for Brave Search API.

        Returns:
            dict: The search results or error message.
            :param count:
        """

        request = WebSearchRequest(q=query, count=count)
        response = await self.bs.web(request)

        search_results = []

        # Print the search results
        for result in response.web.results if response.web else []:
            search_results.append({
                'title': result.title,
                'url': result.url
            })

        return search_results


import os
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
import json


class SerplyNewsSearchToolSchema(BaseModel):
    query: str = Field(..., description="The search query to look for news")
    num_results: int = Field(default=5, description="Number of results to return")


class SerplyNewsSearchTool(BaseTool):
    name: str = "serply_news_search_tool"
    description: str = "A tool that searches for news articles using the Serply API"
    args_schema: Type[BaseModel] = SerplyNewsSearchToolSchema

    def _run(self, query: str, num_results: int = 5) -> str:
        api_key = os.getenv("SERPLY_API_KEY")
        if not api_key:
            raise ValueError("SERPLY_API_KEY environment variable is not set")

        url = "https://serply.io/api/v1/news/search"
        params = {
            "q": query,
            "num": num_results,
            "api_key": api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "news_results" not in data:
                return "No news results found"

            results = []
            for item in data["news_results"]:
                result = {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": item.get("source", ""),
                    "date": item.get("date", "")
                }
                results.append(result)

            return json.dumps(results, indent=2)

        except requests.exceptions.RequestException as e:
            return f"Error performing news search: {str(e)}"


if __name__ == "__main__":
    # Test the tool
    tool = SerplyNewsSearchTool()
    result = tool.run(query="AI news", num_results=3)
    print(result) 
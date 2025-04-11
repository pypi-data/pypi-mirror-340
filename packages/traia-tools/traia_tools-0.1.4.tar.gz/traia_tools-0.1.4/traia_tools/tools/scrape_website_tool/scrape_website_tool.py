from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from bs4 import BeautifulSoup


class ScrapeWebsiteToolSchema(BaseModel):
    url: str = Field(..., description="The URL of the website to scrape")
    selector: str = Field(default="body", description="CSS selector to target specific content")


class ScrapeWebsiteTool(BaseTool):
    name: str = "scrape_website_tool"
    description: str = "A tool that scrapes content from a website"
    args_schema: Type[BaseModel] = ScrapeWebsiteToolSchema

    def _run(self, url: str, selector: str = "body") -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            selected_content = soup.select(selector)

            if not selected_content:
                return f"No content found for selector: {selector}"

            # Extract text from all matching elements
            content = []
            for element in selected_content:
                # Get text and clean it
                text = element.get_text(separator=' ', strip=True)
                if text:
                    content.append(text)

            return '\n\n'.join(content)

        except requests.exceptions.RequestException as e:
            return f"Error scraping website: {str(e)}"


if __name__ == "__main__":
    # Test the tool
    tool = ScrapeWebsiteTool()
    result = tool.run(url="https://example.com", selector="p")
    print(result) 
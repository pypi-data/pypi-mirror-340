from typing import Optional, Dict, Any
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import json
import os

class JSONSearchTool(BaseTool):
    """A tool for searching within JSON files."""
    
    name: str = "json_search_tool"
    description: str = "A tool for searching within JSON files"
    
    class Config(BaseModel):
        json_path: Optional[str] = Field(
            default=None,
            description="Path to the JSON file to search in"
        )
        config: Optional[Dict[str, Any]] = Field(
            default=None,
            description="Configuration for the tool including LLM and embedder settings"
        )
    
    def __init__(self, json_path: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.json_path = json_path
        self.config = config or {}
    
    def _run(self, query: str) -> str:
        """Search within the JSON file using the provided query."""
        if not self.json_path:
            return "Error: No JSON file path provided. Please initialize the tool with a json_path."
        
        if not os.path.exists(self.json_path):
            return f"Error: JSON file not found at {self.json_path}"
        
        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            
            # Basic search implementation - can be enhanced with more sophisticated search logic
            results = self._search_json(data, query)
            
            if not results:
                return f"No results found for query: {query}"
            
            return json.dumps(results, indent=2)
        
        except json.JSONDecodeError:
            return f"Error: Invalid JSON file at {self.json_path}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _search_json(self, data: Any, query: str) -> list:
        """Recursively search through JSON data for matches."""
        results = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if query.lower() in str(key).lower():
                    results.append({key: value})
                if isinstance(value, (dict, list)):
                    results.extend(self._search_json(value, query))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    results.extend(self._search_json(item, query))
                elif query.lower() in str(item).lower():
                    results.append(item)
        
        return results 
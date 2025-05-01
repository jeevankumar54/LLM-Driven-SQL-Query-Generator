import httpx
import json
from typing import Dict, List, Any, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_version = "/api"
        self.timeout = 30.0
    
    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}{self.api_version}{endpoint}"
    
    def _handle_response(self, response: httpx.Response):
        response.raise_for_status()
        return response.json()
    
    def generate_sql(self, natural_language_query: str, schema_id: Optional[int] = None):
        url = self._get_url("/query/generate")
        payload = {
            "natural_language_query": natural_language_query
        }
        
        if schema_id:
            payload["schema_id"] = schema_id
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                return self._handle_response(response)
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP Error: {e.response.status_code}",
                "sql": "",
                "explanation": str(e)
            }
        except Exception as e:
            return {
                "error": "Failed to generate SQL query",
                "sql": "",
                "explanation": str(e)
            }
    
    def execute_sql(self, sql_query: str, schema_id: int):
        url = self._get_url("/query/execute")
        payload = {
            "sql": sql_query,
            "schema_id": schema_id
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                return self._handle_response(response)
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP Error: {e.response.status_code}",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error: {str(e)}",
                "data": None
            }
    
    def get_query_history(self, skip: int = 0, limit: int = 100):
        url = self._get_url(f"/query/history?skip={skip}&limit={limit}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except Exception as e:
            return []
    
    def get_query_by_id(self, query_id: int):
        url = self._get_url(f"/query/history/{query_id}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except Exception as e:
            return None
    
    def get_schemas(self, skip: int = 0, limit: int = 100):
        url = self._get_url(f"/schema?skip={skip}&limit={limit}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response).get("schemas", [])
        except Exception as e:
            return []
    
    def get_schema_by_id(self, schema_id: int):
        url = self._get_url(f"/schema/{schema_id}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except Exception as e:
            return None
    
    def create_schema(self, schema_data: Dict[str, Any]):
        url = self._get_url("/schema")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=schema_data)
                return self._handle_response(response)
        except Exception as e:
            return None
    
    def update_schema(self, schema_id: int, schema_data: Dict[str, Any]):
        url = self._get_url(f"/schema/{schema_id}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.put(url, json=schema_data)
                return self._handle_response(response)
        except Exception as e:
            return None
    
    def delete_schema(self, schema_id: int):
        url = self._get_url(f"/schema/{schema_id}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.delete(url)
                return self._handle_response(response)
        except Exception as e:
            return False
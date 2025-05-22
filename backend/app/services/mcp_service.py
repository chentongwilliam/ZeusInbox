import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class MCPService:
    def __init__(self):
        self.server_url = os.getenv("MCP_SERVER_URL", "http://localhost:3000")
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        response = requests.get(f"{self.server_url}/tools")
        if response.status_code != 200:
            raise Exception("Failed to get available tools")
        return response.json()

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool with given parameters"""
        response = requests.post(
            f"{self.server_url}/execute/{tool_name}",
            json={
                "params": params,
                "api_key": self.api_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Failed to execute tool {tool_name}")
        return response.json()

    async def translate_email(self, content: str, target_language: str) -> str:
        """Translate email content using MCP translation tool"""
        result = await self.execute_tool("translate", {
            "content": content,
            "target_language": target_language
        })
        return result["translated_text"]

    async def classify_email(self, content: str) -> Dict[str, Any]:
        """Classify email content using MCP classification tool"""
        result = await self.execute_tool("classify", {
            "content": content
        })
        return result

    async def summarize_email(self, content: str) -> str:
        """Summarize email content using MCP summarization tool"""
        result = await self.execute_tool("summarize", {
            "content": content
        })
        return result["summary"]

    async def suggest_reply(self, content: str, context: Dict[str, Any] = None) -> str:
        """Generate reply suggestion using MCP suggestion tool"""
        result = await self.execute_tool("suggest_reply", {
            "content": content,
            "context": context or {}
        })
        return result["suggestion"] 
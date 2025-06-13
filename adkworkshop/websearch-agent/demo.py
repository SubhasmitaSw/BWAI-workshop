import os
import logging
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

# Create a simple demo to test the agent
def main():
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    agent = LlmAgent(
        model=LiteLlm(model="ollama_chat/gemma3:latest"),   
        name='websearch_agent',
        description="An agent that can help with web search queries using the MCP toolset.",
        instruction='You are a specialized assistant having access to web search tools to perform web search for queries. When responding to user queries, provide a curated answer by summarizing the search results and extracting the most relevant information.',
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPServerParams(
                    url=os.getenv('MCP_SERVER_URL', 'http://localhost:8080/mcp')
                )
            )
        ],
    )

    # Simulate a search query using MCPToolset
    query = "current weather in Delhi"
    logging.info(f"--- 🔍 Searching for: {query} ---")
    

if __name__ == "__main__":
    main()

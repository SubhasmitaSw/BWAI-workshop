import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.models.lite_llm import LiteLlm

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = (
    'You are a specialized assistant for web search tasks. '
    "Your sole purpose is to use the 'web_search' tool to answer questions about general knowledge and information retrieval. "
    'If the user asks about anything other than web search or general knowledge, '
    'politely state that you cannot help with that topic and can only assist with web search-related queries. '
    'Do not attempt to answer unrelated questions or use tools for other purposes.'
)
def create_agent() -> LlmAgent:
    """Constructs the ADK web search agent."""
    logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
    logger.info("--- 🤖 Creating ADK Web Search Agent... ---")
    return LlmAgent(
        model=LiteLlm(model="ollama_chat/gemma3:latest", response_mode="tool_output"),
        name='web_search_agent',
        description="An agent that can help with web search tasks",
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPServerParams(
                    url=os.getenv('MCP_SERVER_URL', 'http://localhost:8080/mcp')
                )
            )
        ]
    )

root_agent = create_agent()

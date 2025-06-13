# test to check if the server is running 

import asyncio
from fastmcp import Client

async def test_server():
    # Test the MCP server using streamable-http transport.
    async with Client("http://localhost:8080/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f"--- 🛠️  Tool found: {tool.name} ---")
        
        # Call search tool
        print("--- 🔍  Calling search tool for 'Python programming' ---")
        result = await client.call_tool("search", {"query": "Python programming", "limit": 5})
        print(f"--- ✅  Success: {result[0].text} ---")

if __name__ == "__main__":
    asyncio.run(test_server())
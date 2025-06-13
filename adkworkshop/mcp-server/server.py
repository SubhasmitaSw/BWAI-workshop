#!/usr/bin/env python3

import asyncio
import json
from typing import Any, Dict, List
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP

@dataclass
class SearchResult:
    title: str
    url: str
    description: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description
        }

# Create FastMCP instance
mcp = FastMCP("Web Search")

async def perform_search(query: str, limit: int = 5) -> List[SearchResult]:
    """Perform DuckDuckGo search and parse results."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "q": query
    }

    print(f"[DEBUG] Searching DuckDuckGo for: '{query}' with limit: {limit}")

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(
            "https://html.duckduckgo.com/html/",
            data=data,
            headers=headers
        )
        print(f"[DEBUG] Response status: {response.status_code}")
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    containers = soup.select("div.result")
    print(f"[DEBUG] Found {len(containers)} DuckDuckGo result containers")

    for i, container in enumerate(containers):
        if i >= limit:
            break

        # Extract title and URL
        title_element = container.select_one(".result__title a")
        if not title_element:
            continue
        title = title_element.get_text(strip=True)
        url = title_element.get("href", "").strip()

        # Extract description if available
        description_element = container.select_one(".result__snippet")
        description = description_element.get_text(strip=True) if description_element else ""

        if title and url:
            results.append(SearchResult(
                title=title,
                url=url,
                description=description
            ))
            print(f"[DEBUG] Added result {i+1}: {title[:50]}...")

    print(f"[DEBUG] Total results returned: {len(results)}")
    return results

@mcp.tool()
async def search(query: str, limit: int = 5) -> str:
    """
    Search the web using Google.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return (1-10, default: 5)
    
    Returns:
        JSON string containing search results
    """
    if not query or not isinstance(query, str):
        return json.dumps({"error": "Query must be a non-empty string"})
    
    if not isinstance(limit, int) or limit < 1 or limit > 10:
        limit = 5
    
    try:
        results = await perform_search(query, limit)
        results_dict = [result.to_dict() for result in results]
        
        return json.dumps({
            "query": query,
            "results": results_dict,
            "count": len(results_dict)
        }, indent=2)
        
    except httpx.RequestError as error:
        return json.dumps({"error": f"Search request failed: {str(error)}"})
    except Exception as error:
        return json.dumps({"error": f"Search failed: {str(error)}"})

# Add a simple health check endpoint
@mcp.tool()
async def health() -> str:
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return json.dumps({"status": "healthy", "service": "web-search-api"})

if __name__ == "__main__":
    import uvicorn
    
    # Get the FastAPI app from FastMCP
    app = mcp.http_app()
    
    # Run with uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        log_level="info"
    )
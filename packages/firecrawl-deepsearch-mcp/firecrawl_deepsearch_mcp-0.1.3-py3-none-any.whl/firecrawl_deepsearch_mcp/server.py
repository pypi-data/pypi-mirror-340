import os
import logging
from firecrawl import FirecrawlApp
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("Firecrawl Deepsearch MCP", dependencies=[
    "firecrawl",
])

@mcp.tool()
def deepsearch(system_prompt: str, user_message: str) -> str:
    """Performs a deep search using Firecrawl based on the provided prompts."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        logger.error("FIRECRAWL_API_KEY environment variable not set.")
        return "Error: FIRECRAWL_API_KEY environment variable must be configured."

    try:
        kwargs = {"api_key": api_key}
        if os.getenv("DEV_MODE") == "true":
            kwargs["api_url"] = "http://localhost:3001"
        
        client = FirecrawlApp(**kwargs)
        
        # Define search parameter tiers
        search_params = {
            "quick": {"maxDepth": 2, "timeLimit": 30, "maxUrls": 5},
            "balanced": {"maxDepth": 5, "timeLimit": 120, "maxUrls": 50}, # Medium values
            "thorough": {"maxDepth": 10, "timeLimit": 300, "maxUrls": 300}
        }

        # Select search strength based on environment variable
        search_strength = os.getenv("SEARCH_STRENGTH", "balanced").lower()
        if search_strength not in search_params:
            logger.warning(f"Invalid SEARCH_STRENGTH '{search_strength}'. Defaulting to 'balanced'.")
            search_strength = "balanced"
        
        params = search_params[search_strength]
        logger.info(f"Using search strength '{search_strength}' with params: {params}")

        def _on_activity(activity):
            logger.info(f"[Firecrawl {activity['type']}] {activity['message']}")

        search_query = f"{system_prompt}\n\n{user_message}"
        logger.info(f"Performing Firecrawl deep research with query: {search_query[:100]}...") # Log truncated query

        results = client.deep_research(
            query=search_query,
            params=params,
            on_activity=_on_activity
        )

        if not results or 'data' not in results:
            logger.error("Received invalid response structure from Firecrawl")
            return "Error: Invalid response from Firecrawl"

        final_analysis = results['data'].get('finalAnalysis', 'No analysis provided.')
        sources = results['data'].get('sources', [])
        
        response = f"{final_analysis}\n\nSources consulted: {len(sources)} references"
        logger.info("Firecrawl deep research completed successfully.")
        return response

    except Exception as e:
        logger.exception(f"Firecrawl search failed: {e}")
        return f"Error during Firecrawl search: {e}"


def main():
    mcp.run()

if __name__ == "__main__":
    main()
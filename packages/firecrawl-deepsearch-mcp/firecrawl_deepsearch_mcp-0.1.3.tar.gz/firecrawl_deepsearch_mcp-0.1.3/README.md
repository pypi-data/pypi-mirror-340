# firecrawl-deepsearch-mcp MCP server

Deepsearch by firecrawl. MCP server

## Usage

### For MCP Client Users

To use this server with your preferred MCP client (like Claude Desktop), add the following configuration to your client's MCP server settings:

```json
{
  "mcpServers": {
    "Firecrawl Deepsearch MCP": {
      "command": "uvx",
      "args": ["firecrawl-deepsearch-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "fc-XXXXXX" 
      }
    }
  }
}
```

**Important:** Replace `"fc-XXXXXX"` with your actual Firecrawl API key.

### Environment Variables

The server's behavior can be configured using the following environment variables:

*   `FIRECRAWL_API_KEY` (**Required**): Your API key for accessing the Firecrawl service. You can obtain one from [firecrawl.dev](https://firecrawl.dev/). The server will return an error if this is not set.
*   `SEARCH_STRENGTH` (Optional): Controls the depth and resource usage of the Firecrawl deep research. Defaults to `"balanced"`.
    *   `"quick"`: Fastest search, shallow depth (maxDepth: 2, timeLimit: 30s, maxUrls: 5).
    *   `"balanced"`: Medium depth and time (maxDepth: 5, timeLimit: 120s, maxUrls: 50). Recommended for most use cases.
    *   `"thorough"`: Most comprehensive search, highest depth and time (maxDepth: 10, timeLimit: 300s, maxUrls: 300). Use when detailed results are critical.
*   `DEV_MODE` (Optional): If set to `"true"`, the server will attempt to connect to a local Firecrawl instance at `http://localhost:3001` instead of the default production API URL. Useful for developing or testing against a local Firecrawl deployment.

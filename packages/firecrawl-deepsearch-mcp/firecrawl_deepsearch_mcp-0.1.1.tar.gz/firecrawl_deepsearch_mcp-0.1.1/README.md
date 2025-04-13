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

## Components

### Resources

The server implements a simple note storage system with:
- Custom note:// URI scheme for accessing individual notes
- Each note resource has a name, description and text/plain mimetype

### Prompts

The server provides a single prompt:
- summarize-notes: Creates summaries of all stored notes
  - Optional "style" argument to control detail level (brief/detailed)
  - Generates prompt combining all current notes with style preference

### Tools

The server implements one tool:
- add-note: Adds a new note to the server
  - Takes "name" and "content" as required string arguments
  - Updates server state and notifies clients of resource changes

## Configuration

[TODO: Add configuration details specific to your implementation]

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "firecrawl-deepsearch-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/tolik/Code/firecrawl-deepsearch-mcp",
        "run",
        "firecrawl-deepsearch-mcp"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "firecrawl-deepsearch-mcp": {
      "command": "uvx",
      "args": [
        "firecrawl-deepsearch-mcp"
      ]
    }
  }
  ```
</details>

## Development

### Prerequisites

*   Python >= 3.12
*   [AWS CLI](https://aws.amazon.com/cli/) installed and configured with appropriate permissions for CodeArtifact.
*   Python build tool: `pip install build`
*   Python publishing tool: `pip install twine` (or install via `uv add twine` if using `uv`).

### AWS CodeArtifact Setup

These steps only need to be performed once for your AWS account and region.

1.  **Set Default Region (Optional but recommended):**
    ```bash
    export AWS_DEFAULT_REGION=<your-aws-region> 
    # e.g., export AWS_DEFAULT_REGION=us-east-1
    ```

2.  **Create CodeArtifact Domain:**
    A domain groups repositories. Choose a unique name.
    ```bash
    aws codeartifact create-domain --domain <your-domain-name>
    # Example: aws codeartifact create-domain --domain mcp-servers
    ```

3.  **Create CodeArtifact Repository:**
    This repository will store your package. Choose a name (e.g., the package name).
    ```bash
    aws codeartifact create-repository --domain <your-domain-name> --repository <your-repository-name>
    # Example: aws codeartifact create-repository --domain mcp-servers --repository firecrawl-deepsearch-mcp
    ```
    *(Optional: Add `--upstreams repositoryName=pypi` to allow pulling packages from the public PyPI through this repository).*


### Publishing to AWS CodeArtifact

1.  **Login to CodeArtifact with Twine:**
    This command retrieves temporary credentials and configures `twine` (via `~/.pypirc`) to use your repository. Run this periodically (e.g., every 12 hours or when credentials expire).
    ```bash
    aws codeartifact login --tool twine --domain <your-domain-name> --domain-owner <your-aws-account-id> --repository <your-repository-name>
    # Example: aws codeartifact login --tool twine --domain mcp-servers --domain-owner 211324922397 --repository firecrawl-deepsearch-mcp
    ```
    *(Note: Replace `<your-aws-account-id>` with your actual AWS Account ID)*.

2.  **Build the Package:**
    This creates the distributable files (`.whl`, `.tar.gz`) in the `dist/` directory. Use `uv` if you manage dependencies with it, otherwise use `python -m build`.
    ```bash
    # If using uv
    uv build
    ```

3.  **Upload using Twine:**
    Use the repository alias configured by the `login` command (usually `codeartifact`).
    ```bash
    twine upload --repository codeartifact dist/*
    ```

### Testing the Published Package

After publishing and logging into CodeArtifact with `uv` (`aws codeartifact login --tool uv ...`), you can test if the package is installable and importable from your repository using `uv run`:

```bash
uv run --with firecrawl-deepsearch-mcp --no-project -- python -c "import firecrawl_deepsearch_mcp"
```

This command creates a temporary environment, installs your package (`--with firecrawl-deepsearch-mcp`), ignores any local project file (`--no-project`), and runs a simple Python command to check if the package's main module can be imported.

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/tolik/Code/firecrawl-deepsearch-mcp run firecrawl-deepsearch-mcp
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.# firecrawl-deepsearch-mcp

# Network Call Analyzer MCP Server

A Model Context Protocol server that analyzes network traffic for a given URL using Playwright. This server enables LLMs to understand the resources loaded by a webpage.

### Available Tools

- `analyze_network` - Analyzes network traffic for a URL using Playwright.
    - `url` (string, required): URL to analyze.
    - `filters` (string, optional): Comma-separated list of file extensions or content types to filter out (e.g., css,png,woff).

### Prompts

- **analyze_network**
  - Analyze network traffic for a URL.
  - Arguments:
    - `url` (string, required): URL to analyze.

## Installation

Requires Node.js and Playwright to be installed.

1. Install Playwright browsers:
   ```bash
   playwright install --with-deps chromium
   # Or: python -m playwright install --with-deps chromium
   ```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *network-call-analyzer*.

### Using PIP

Alternatively you can install `network-call-analyzer` via pip:

```
uv pip install .
```

After installation, you can run it as a script using:

```
python -m network_call_analyzer_mcp
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "network_analyzer": {
    "command": "uvx",
    "args": ["network-call-analyzer"]
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "network_analyzer": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "your-docker-image-name"] # TODO: Update docker image name
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "network_analyzer": {
    "command": "python",
    "args": ["-m", "network_call_analyzer_mcp"]
  }
}
```
</details>

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx network-call-analyzer
```

Or if you've installed the package in a specific directory or are developing on it:

```
cd path/to/servers/src/network_call_analyzer # Adjust path if needed
npx @modelcontextprotocol/inspector uv run network-call-analyzer
```

## Contributing

We encourage contributions to help expand and improve network-call-analyzer. Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

Pull requests are  not welcome! This is meant to be a throw away package that it shall work as such

## License

network-call-analyzer is licensed under the Better than MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the Better than MIT License. For more details, please see the LICENSE file in the project repository.

import asyncio
import json
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from typing import List, Dict, Any, Annotated

from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field, AnyUrl


class NetworkTrafficAnalyzer:
    """Analyzes network traffic for a given URL using Playwright."""

    def __init__(self, url: str, filters: List[str]):
        self.url = str(url) # Ensure url is string
        self.filters = [f.strip().lower() for f in filters]
        self.network_traffic: List[Dict[str, Any]] = []
        self._requests_data: Dict[str, Dict[str, Any]] = {}

    def _should_filter_request(self, url: str, content_type: str) -> bool:
        """Check if the request should be filtered based on extension or content type."""
        parsed_url = urlparse(url)
        extension = (
            parsed_url.path.split(".")[-1].lower() if "." in parsed_url.path else ""
        )

        if extension in self.filters:
            return True

        if content_type:
            content_type = content_type.split(';')[0].strip().lower() # Handle 'text/html; charset=utf-8'
            for filter_item in self.filters:
                if filter_item == extension or filter_item in content_type:
                    return True

        return False

    async def analyze_traffic(self) -> Dict[str, Any]:
        """Launches Playwright, navigates to URL, and collects network traffic."""
        try:
            async with async_playwright() as p:
                # Try launching with system Chromium first if available
                try:
                    browser = await p.chromium.launch()
                except Exception:
                    # Fallback: Ensure browsers are installed if launch fails
                    # This might happen in environments where install wasn't run
                    print("Chromium launch failed, attempting to install...")
                    import subprocess
                    subprocess.run(["playwright", "install", "--with-deps", "chromium"], check=True)
                    print("Playwright install finished, retrying launch...")
                    browser = await p.chromium.launch()

                page = await browser.new_page()

                # Listen to network events
                async def handle_request(request):
                    self._requests_data[request.url] = {
                        "url": request.url,
                        "method": request.method,
                        "time_start": asyncio.get_event_loop().time(),
                    }

                async def handle_response(response):
                    request = response.request
                    if request.url in self._requests_data:
                        time_end = asyncio.get_event_loop().time()
                        time_start = self._requests_data[request.url]["time_start"]

                        try:
                            headers = await response.all_headers()
                            content_type = headers.get("content-type", "")
                            content_length = int(headers.get("content-length", 0))

                            if not self._should_filter_request(
                                request.url, content_type
                            ):
                                self.network_traffic.append(
                                    {
                                        "url": request.url,
                                        "method": request.method,
                                        "status": response.status,
                                        "contentType": content_type,
                                        "size_bytes": content_length,
                                        "duration_ms": int(
                                            (time_end - time_start) * 1000
                                        ), # Convert to milliseconds
                                    }
                                )
                        except Exception as e:
                            # Log error processing a specific response but continue
                            print(f"Error processing response for {request.url}: {str(e)}")
                        finally:
                            # Clean up processed request data
                            del self._requests_data[request.url]

                page.on("request", handle_request)
                page.on("response", handle_response)

                # Navigate to the URL
                try:
                    await page.goto(self.url, wait_until="networkidle", timeout=60000) # 60s timeout
                except Exception as nav_error:
                     # Catch navigation errors specifically
                    await browser.close()
                    raise McpError(ErrorData(
                        code=INTERNAL_ERROR,
                        message=f"Error navigating to {self.url}: {str(nav_error)}"
                    ))

                # Wait a bit for any final network requests after networkidle
                await asyncio.sleep(3)

                await browser.close()

                return {"status": "Success", "network_traffic": self.network_traffic}

        except Exception as e:
            # Catch broader Playwright/setup errors
            error_message = f"Error during Playwright operation: {str(e)}"
            print(error_message) # Log for debugging
            raise McpError(ErrorData(
                code=INTERNAL_ERROR,
                message=error_message,
            ))


class AnalyzeNetworkParams(BaseModel):
    """Parameters for analyzing network traffic."""
    url: Annotated[AnyUrl, Field(description="URL to analyze.")]
    filters: Annotated[
        str, Field(default="", description="Comma-separated list of file extensions or content types to filter out (e.g., css,png,woff).")
    ]


async def serve() -> None:
    """Run the network analyzer MCP server."""
    server = Server("network-call-analyzer")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="analyze_network",
                description="Analyzes network traffic for a given URL using Playwright, returning a list of network requests (excluding filtered types). Useful for understanding what resources a webpage loads.",
                inputSchema=AnalyzeNetworkParams.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="analyze_network",
                description="Analyze network traffic for a URL.",
                arguments=[
                    PromptArgument(
                        name="url", description="URL to analyze", required=True
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name != "analyze_network":
             raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Unknown tool: {name}"))

        try:
            args = AnalyzeNetworkParams(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        url = str(args.url)
        if not url:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

        filter_list = [f.strip().lower() for f in args.filters.split(',') if f.strip()]

        try:
            analyzer = NetworkTrafficAnalyzer(url=url, filters=filter_list)
            result = await analyzer.analyze_traffic()

            # analyze_traffic now raises McpError on failure
            # The result format assumes success if no exception is raised
            traffic_json = json.dumps(result.get("network_traffic", []), indent=2)
            return [TextContent(type="text", text=f"Network analysis complete for {url}. Filtered types: {args.filters or 'None'}.\n\nTraffic:\n```json\n{traffic_json}\n```")]

        except McpError as e:
            # Re-raise McpErrors directly
            raise e
        except Exception as e:
            # Catch any other unexpected errors during analysis
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Unexpected error during analysis: {str(e)}"))


    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if name != "analyze_network":
            # In a real scenario, you might have multiple prompts
            return GetPromptResult(description=f"Unknown prompt: {name}", messages=[])

        if not arguments or "url" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL argument is required for the analyze_network prompt"))

        url = str(arguments["url"]) # Ensure url is string
        filters = arguments.get("filters", "") # Optional filters for prompt too?
        filter_list = [f.strip().lower() for f in filters.split(',') if f.strip()]

        try:
            analyzer = NetworkTrafficAnalyzer(url=url, filters=filter_list)
            result = await analyzer.analyze_traffic()
            traffic_json = json.dumps(result.get("network_traffic", []), indent=2)
            content = f"Network analysis complete for {url}. Filtered types: {filters or 'None'}.\n\nTraffic:\n```json\n{traffic_json}\n```"
            return GetPromptResult(
                description=f"Network Traffic for {url}",
                messages=[
                    PromptMessage(
                        role="user", content=TextContent(type="text", text=content)
                    )
                ],
            )
        except McpError as e:
            # Return error information within the prompt structure
            return GetPromptResult(
                description=f"Error analyzing {url}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=f"Failed to analyze network for {url}:\n{e.data.message}"),
                    )
                ],
            )
        except Exception as e:
             # Catch unexpected errors
            return GetPromptResult(
                description=f"Unexpected Error analyzing {url}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=f"An unexpected error occurred: {str(e)}"),
                    )
                ],
            )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

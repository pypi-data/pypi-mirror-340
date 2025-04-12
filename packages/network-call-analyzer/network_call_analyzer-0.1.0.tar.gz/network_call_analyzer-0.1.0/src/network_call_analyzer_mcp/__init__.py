from .server import serve


def main():
    """MCP Network Call Analyzer Server - Playwright-based network analysis for MCP"""
    import argparse
    import asyncio

    # Although no command-line arguments are currently defined for serve,
    # we keep the argparse structure for future extensibility.
    parser = argparse.ArgumentParser(
        description="Analyze network traffic for a URL using Playwright via MCP"
    )
    # Example: Add arguments if needed later
    # parser.add_argument("--some-option", type=str, help="Description")

    args = parser.parse_args()

    # Pass parsed args to serve if it accepts them in the future
    # For now, serve() takes no arguments matching this structure.
    asyncio.run(serve())


if __name__ == "__main__":
    main()

from . import server

def main():
    """Main entry point for the package."""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="MCP server to work with Obsidian remotely via REST plugin"
    )
    # Add arguments if needed
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio", # Default to stdio
        choices=["stdio", "sse"], # Restrict choices
        help="Transport mechanism: stdio or sse (default: stdio)"
    )

    args = parser.parse_args()
    server.main(transport=args.transport)

if __name__ == "__main__":
    main()

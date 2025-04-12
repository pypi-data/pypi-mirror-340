"""Flyder MCP Server Package."""

from . import server

__version__ = "0.4.2"
__all__ = ["main", "server"]


def main():
    """Main entry point for the package."""
    import os
    import sys
    import logging
    
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Check for required environment variables
    if not os.getenv("FLYDER_EMAIL"):
        logging.error("Environment variable FLYDER_EMAIL is not set")
        sys.exit(1)
    
    if not os.getenv("FLYDER_API_KEY"):
        logging.error("Environment variable FLYDER_API_KEY is not set")
        sys.exit(1)
    
    logging.info(f"Starting mcp-server-flyder v{__version__}")
    server.mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
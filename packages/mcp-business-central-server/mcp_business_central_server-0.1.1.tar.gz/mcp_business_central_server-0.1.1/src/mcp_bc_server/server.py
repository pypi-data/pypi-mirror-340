import asyncio
from .common import logger, mcp

async def run_server():
    """Main async function to run the server"""
    # Log server startup
    logger.info("Starting Business Central MCP server ...")
    
    # Import tools and resources 
    from . import resources, tools
    
    # Run the mcp server
    logger.info("Running MCP server...")
    await mcp.run_stdio_async()

def main():
    """Entry point for the command line script"""
    asyncio.run(run_server())

if __name__ == "__main__":
    # Direct script execution entry point
    main()
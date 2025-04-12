#!/usr/bin/env python3
"""
OpenCV MCP Server - Entry Point

This module initializes and configures the FastMCP server for the OpenCV MCP implementation,
importing and registering all tools from other modules, setting up server capabilities,
and handling server lifecycle management.
"""

import os
import sys
import logging
from mcp.server.fastmcp import FastMCP

# Import tool modules
import image_basics
# import image_processing
# import computer_vision
# import video_processing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("opencv-mcp-server")
mcp = FastMCP(
    name="opencv-mcp-server",
    description="MCP server providing OpenCV computer vision capabilities",
)
def main():
    """
    Initialize and run the OpenCV MCP server
    """
    # Create FastMCP server instance

    # Register all tools from modules
    register_tools(mcp)
    
    # Configure server options
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    logger.info(f"Starting OpenCV MCP server with transport: {transport}")
    
    # Run the server
    mcp.run(transport=transport)

def register_tools(mcp):
    """
    Register all tools from the imported modules
    """
    logger.info("Registering OpenCV tools")
    
    # Register image basics tools
    logger.info("Registering image basics tools")
    image_basics.register_tools(mcp)
    
    # # Register image processing tools
    # logger.info("Registering image processing tools")
    # image_processing.register_tools(mcp)
    
    # # Register computer vision tools
    # logger.info("Registering computer vision tools")
    # computer_vision.register_tools(mcp)
    
    # # Register video processing tools
    # logger.info("Registering video processing tools")
    # video_processing.register_tools(mcp)
    
    logger.info("All tools registered successfully")

if __name__ == "__main__":
    main()
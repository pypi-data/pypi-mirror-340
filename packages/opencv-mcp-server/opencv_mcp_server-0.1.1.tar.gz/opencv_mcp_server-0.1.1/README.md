# OpenCV MCP Server

MCP server providing OpenCV computer vision capabilities.


![](https://badge.mcpx.dev?type=server 'MCP Server')


## Introduction

OpenCV MCP Server is a Python package that provides OpenCV's image and video processing capabilities through the Model Context Protocol (MCP). This allows AI assistants and language models to access powerful computer vision tools.

## Features

- Basic image handling and manipulation (read, save, convert)
- Image processing (resize, crop, filter application)
- Advanced computer vision capabilities (feature detection, object detection)
- Video processing and analysis

## Installation

```bash
pip install opencv-mcp-server
```

## Usage

### Use in Claude Desktop

```json
    "opencv": {
      "command": "uvx",
      "args": [
        "opencv-mcp-server"
      ]
    }
```

### Configuration

The server can be configured using environment variables:

- `MCP_TRANSPORT`: Transport method (default: "stdio")

## Available Tools

- `save_image_tool`: Save an image to a file
- `convert_color_space_tool`: Convert image between color spaces
- `resize_image_tool`: Resize an image to specific dimensions
- `crop_image_tool`: Crop a region from an image
- `get_image_stats_tool`: Get statistical information about an image

More tools will be added in future releases.

## License

MIT License

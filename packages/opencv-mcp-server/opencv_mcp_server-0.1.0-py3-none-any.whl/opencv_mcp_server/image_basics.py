"""
OpenCV MCP Server - Image Basics

This module provides basic image handling and manipulation tools using OpenCV.
It includes functionality for reading, saving, and manipulating images.
"""

import cv2
import numpy as np
import os
import logging
import datetime
import subprocess
import platform
from typing import Optional, Dict, Any, List, Union
from .main import mcp

logger = logging.getLogger("opencv-mcp-server.image_basics")

# Utility Functions
def get_image_info(image: np.ndarray) -> Dict[str, Any]:
    """
    Get basic information about an image
    
    Args:
        image: OpenCV image
        
    Returns:
        Dict: Image information including dimensions, channels, etc.
    """
    if image is None:
        raise ValueError("Image is None")
    
    height, width = image.shape[:2]
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    dtype = str(image.dtype)
    size_bytes = image.nbytes
    
    return {
        "width": width,
        "height": height,
        "channels": channels,
        "dtype": dtype,
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2)
    }

def get_timestamp() -> str:
    """
    Get current timestamp as a string
    
    Returns:
        str: Formatted timestamp
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def open_image_with_system_viewer(image_path: str) -> None:
    """
    Open an image with the system's default image viewer
    
    Args:
        image_path: Path to the image file
    """
    # Platform-specific image opening commands
    system = platform.system()
    
    try:
        if system == 'Windows':
            os.startfile(image_path)
        elif system == 'Darwin':  # macOS
            subprocess.call(['open', image_path])
        else:  # Linux and other Unix-like systems
            subprocess.call(['xdg-open', image_path])
        
        logger.info(f"Opened image: {image_path}")
    except Exception as e:
        logger.error(f"Error opening image with system viewer: {e}")
        # Continue execution even if display fails

def save_and_display(img: np.ndarray, original_path: str, operation: str) -> str:
    """
    Save image to file and display it using system's default image viewer
    
    Args:
        img: OpenCV image
        original_path: Path to original image
        operation: Name of operation performed
        
    Returns:
        str: Path to saved image
    """
    # Get directory of original image
    directory = os.path.dirname(original_path) or '.'
    
    # Get filename without extension
    base_name = os.path.basename(original_path)
    name_parts = os.path.splitext(base_name)
    
    # Create new filename with operation and timestamp
    timestamp = get_timestamp()
    new_filename = f"{name_parts[0]}_{operation}_{timestamp}{name_parts[1]}"
    new_path = os.path.join(directory, new_filename)
    
    # Save image
    cv2.imwrite(new_path, img)
    
    # Display image using system's default image viewer
    open_image_with_system_viewer(new_path)
    
    return new_path

# Tool implementations
def save_image_tool(path_in: str, path_out: str) -> Dict[str, Any]:
    """
    Save an image to a file
    
    Args:
        path_in: Path to input image
        path_out: Output file path
        
    Returns:
        Dict: Status information
    """
    # Read input image
    img = cv2.imread(path_in)
    if img is None:
        raise ValueError(f"Failed to read image from path: {path_in}")
    
    # Ensure directory exists
    directory = os.path.dirname(path_out)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # Save and display
    new_path = save_and_display(img, path_out, "save")
    
    return {
        "success": True,
        "path": new_path,
        "size_bytes": os.path.getsize(new_path),
        "size_mb": round(os.path.getsize(new_path) / (1024 * 1024), 2),
        "output_path": new_path  # Return path for chaining operations
    }

def convert_color_space_tool(image_path: str, source_space: str, target_space: str) -> Dict[str, Any]:
    """
    Convert image between color spaces
    
    Args:
        image_path: Path to the image file
        source_space: Source color space (BGR, RGB, GRAY, HSV, etc.)
        target_space: Target color space (BGR, RGB, GRAY, HSV, etc.)
        
    Returns:
        Dict: Converted image information and path
    """
    # Read image from path
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")
    
    # Map color space names to OpenCV constants
    color_space_map = {
        "BGR": cv2.COLOR_BGR2BGR,  # Identity
        "RGB": cv2.COLOR_BGR2RGB,
        "GRAY": cv2.COLOR_BGR2GRAY,
        "HSV": cv2.COLOR_BGR2HSV,
        "LAB": cv2.COLOR_BGR2LAB,
        "YCrCb": cv2.COLOR_BGR2YCrCb,
        "XYZ": cv2.COLOR_BGR2XYZ,
        "HSL": cv2.COLOR_BGR2HLS,
        "YUV": cv2.COLOR_BGR2YUV,
    }
    
    # Create reverse mappings
    for src, code in list(color_space_map.items()):
        if src != "BGR":
            color_space_map[src + "_BGR"] = eval(f"cv2.COLOR_{src}2BGR")
    
    # Determine the conversion code
    conversion_key = f"{source_space}_{target_space}"
    if conversion_key in color_space_map:
        conversion_code = color_space_map[conversion_key]
    else:
        # Handle two-step conversion via BGR
        src_to_bgr_key = f"{source_space}_BGR"
        bgr_to_tgt_key = f"BGR_{target_space}"
        
        if src_to_bgr_key in color_space_map and bgr_to_tgt_key in color_space_map:
            # First convert to BGR
            img = cv2.cvtColor(img, color_space_map[src_to_bgr_key])
            # Then convert from BGR to target
            conversion_code = color_space_map[bgr_to_tgt_key]
        else:
            raise ValueError(f"Unsupported color space conversion: {source_space} to {target_space}")
    
    # Perform the conversion
    converted = cv2.cvtColor(img, conversion_code)
    
    # For display purposes, convert back to BGR if not already in BGR
    display_img = converted
    if target_space != "BGR" and f"{target_space}_BGR" in color_space_map:
        display_img = cv2.cvtColor(converted, color_space_map[f"{target_space}_BGR"])
    
    # Save and display
    new_path = save_and_display(display_img, image_path, f"convert_{source_space}_to_{target_space}")
    
    return {
        "source_space": source_space,
        "target_space": target_space,
        "info": get_image_info(converted),
        "path": new_path,
        "output_path": new_path  # Return path for chaining operations
    }

def resize_image_tool(image_path: str, width: int, height: int, interpolation: str = "INTER_LINEAR") -> Dict[str, Any]:
    """
    Resize an image to specific dimensions
    
    Args:
        image_path: Path to the image file
        width: Target width in pixels
        height: Target height in pixels
        interpolation: Interpolation method
        
    Returns:
        Dict: Resized image information and path
    """
    # Read image from path
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")
    
    # Map interpolation methods to OpenCV constants
    interp_methods = {
        "INTER_NEAREST": cv2.INTER_NEAREST,
        "INTER_LINEAR": cv2.INTER_LINEAR,
        "INTER_CUBIC": cv2.INTER_CUBIC,
        "INTER_AREA": cv2.INTER_AREA,
        "INTER_LANCZOS4": cv2.INTER_LANCZOS4
    }
    
    interp = interp_methods.get(interpolation, cv2.INTER_LINEAR)
    
    # Perform the resize
    resized = cv2.resize(img, (width, height), interpolation=interp)
    
    # Save and display
    new_path = save_and_display(resized, image_path, f"resize_{width}x{height}")
    
    return {
        "width": width,
        "height": height,
        "interpolation": interpolation,
        "info": get_image_info(resized),
        "original_info": get_image_info(img),
        "path": new_path,
        "output_path": new_path  # Return path for chaining operations
    }

def crop_image_tool(image_path: str, x: int, y: int, width: int, height: int) -> Dict[str, Any]:
    """
    Crop a region from an image
    
    Args:
        image_path: Path to the image file
        x: X-coordinate of top-left corner
        y: Y-coordinate of top-left corner
        width: Width of crop region
        height: Height of crop region
        
    Returns:
        Dict: Cropped image information and path
    """
    # Read image from path
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")
    
    # Get image dimensions
    img_height, img_width = img.shape[:2]
    
    # Validate crop parameters
    if x < 0 or y < 0 or (x + width) > img_width or (y + height) > img_height:
        raise ValueError(f"Crop region ({x}, {y}, {width}, {height}) is outside image bounds ({img_width}, {img_height})")
    
    # Perform the crop
    cropped = img[y:y+height, x:x+width]
    
    # Save and display
    new_path = save_and_display(cropped, image_path, f"crop_{x}_{y}_{width}_{height}")
    
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "info": get_image_info(cropped),
        "original_info": get_image_info(img),
        "path": new_path,
        "output_path": new_path  # Return path for chaining operations
    }

def get_image_stats_tool(image_path: str, channels: bool = True) -> Dict[str, Any]:
    """
    Get statistical information about an image
    
    Args:
        image_path: Path to the image file
        channels: Whether to calculate stats per channel
        
    Returns:
        Dict: Image statistics and paths
    """
    # Read image from path
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")
    
    # Calculate basic statistics
    info = get_image_info(img)
    
    # Calculate mean and standard deviation
    mean, stddev = cv2.meanStdDev(img)
    
    stats = {
        "info": info,
        "min": float(np.min(img)),
        "max": float(np.max(img)),
        "mean": float(np.mean(img)),
        "stddev": float(np.std(img))
    }
    
    # Calculate per-channel statistics if requested
    if channels and len(img.shape) > 2:
        channel_stats = []
        for i in range(img.shape[2]):
            channel = img[:,:,i]
            channel_stats.append({
                "channel": i,
                "min": float(np.min(channel)),
                "max": float(np.max(channel)),
                "mean": float(np.mean(channel)),
                "stddev": float(np.std(channel))
            })
        stats["channels"] = channel_stats
    
    # Calculate histogram data
    hist_data = []
    if len(img.shape) > 2:  # Color image
        for i in range(img.shape[2]):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            hist_data.append(hist.flatten().tolist())
    else:  # Grayscale image
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_data.append(hist.flatten().tolist())
    
    stats["histogram"] = hist_data
    
    # Create a visual histogram
    hist_img = np.zeros((400, 512, 3), np.uint8)
    hist_img[:] = (255, 255, 255)  # White background
    
    colors = [(255,0,0), (0,255,0), (0,0,255)]  # BGR for each channel
    
    for i, hist_channel in enumerate(hist_data):
        if i >= 3:  # Only handle up to 3 channels
            break
            
        # Normalize histogram for display
        hist_max = max(hist_channel)
        if hist_max > 0:
            normalized = [h * 380 / hist_max for h in hist_channel]
            
            # Draw histogram lines
            for x in range(256):
                pt1 = (2*x, 399)
                pt2 = (2*x, 399 - int(normalized[x]))
                cv2.line(hist_img, pt1, pt2, colors[i], 1)
    
    # Save and display histogram
    hist_path = save_and_display(hist_img, image_path, "histogram")
    
    # Display the original image as well
    display_path = save_and_display(img, image_path, "stats")
    
    stats["histogram_image_path"] = hist_path
    stats["image_path"] = display_path
    stats["output_path"] = display_path  # Return path for chaining operations
    
    return stats

def register_tools(mcp):
    """
    Register all image basics tools with the MCP server
    
    Args:
        mcp: The MCP server instance
    """
    # Register optimized tool implementations
    mcp.add_tool(save_image_tool)
    mcp.add_tool(convert_color_space_tool)
    mcp.add_tool(resize_image_tool)
    mcp.add_tool(crop_image_tool)
    mcp.add_tool(get_image_stats_tool)

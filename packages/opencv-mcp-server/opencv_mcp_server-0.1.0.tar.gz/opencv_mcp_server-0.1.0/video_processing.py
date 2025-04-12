"""
OpenCV MCP Server - Video Processing

This module provides video handling and analysis tools using OpenCV.
It includes functionality for extracting frames, detecting motion,
and tracking objects in videos.
"""

import cv2
import numpy as np
import base64
import os
import logging
from typing import Optional, List, Dict, Any, Tuple, Union
import tempfile

# Import utility functions from image_basics
from image_basics import decode_image, encode_image, get_image_info

logger = logging.getLogger("opencv-mcp-server.video_processing")

# Video utility functions
def decode_video_file(video_base64: str) -> str:
    """
    Decode base64 video to a temporary file
    
    Args:
        video_base64: Base64 encoded video string
        
    Returns:
        str: Path to temporary video file
    """
    try:
        # Decode base64 to binary
        video_data = base64.b64decode(video_base64)
        
        # Create a temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.mp4')
        os.close(fd)
        
        # Write to temporary file
        with open(temp_path, 'wb') as f:
            f.write(video_data)
        
        return temp_path
    except Exception as e:
        logger.error(f"Error decoding video: {str(e)}")
        raise ValueError(f"Failed to decode video: {str(e)}")

def get_video_info(video_path: str) -> Dict[str, Any]:
    """
    Get basic information about a video
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dict: Video information including dimensions, fps, frame count, etc.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        
        # Convert fourcc to readable format
        fourcc = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])
        
        # Calculate duration in seconds
        duration = frame_count / fps if fps > 0 else 0
        
        # Release the capture
        cap.release()
        
        return {
            "width": width,
            "height": height,
            "fps": float(fps),
            "frame_count": frame_count,
            "fourcc": fourcc,
            "duration_seconds": float(duration),
            "duration_formatted": f"{int(duration // 60):02d}:{int(duration % 60):02d}"
        }
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise ValueError(f"Failed to get video info: {str(e)}")

# Tool implementations
def extract_video_frames_tool(
    video_path: str,
    video_base64: Optional[str] = None,
    start_frame: int = 0,
    end_frame: Optional[int] = None,
    step: int = 1,
    max_frames: int = 10
) -> Dict[str, Any]:
    """
    Extract frames from a video file
    
    Args:
        video_path: Path to video file (can be None if video_base64 is provided)
        video_base64: Base64 encoded video string (optional)
        start_frame: Starting frame index (0-based)
        end_frame: Ending frame index (inclusive), if None extracts until the end
        step: Step size (extract every nth frame)
        max_frames: Maximum number of frames to extract
        
    Returns:
        Dict: Extracted frames and video information
    """
    try:
        temp_path = None
        
        # Handle base64 input
        if video_base64 is not None:
            temp_path = decode_video_file(video_base64)
            video_path = temp_path
        
        # Open the video
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        # Get video info
        video_info = get_video_info(video_path)
        total_frames = video_info["frame_count"]
        
        # Validate and adjust parameters
        if start_frame < 0:
            start_frame = 0
        
        if end_frame is None or end_frame >= total_frames:
            end_frame = total_frames - 1
        
        if step < 1:
            step = 1
        
        # Calculate number of frames to extract
        num_frames = min(
            (end_frame - start_frame) // step + 1,
            max_frames
        )
        
        # Extract frames
        frames = []
        
        # Set position to start_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for i in range(num_frames):
            # Calculate the frame index
            frame_idx = start_frame + (i * step)
            
            # Skip if we've reached the end_frame
            if frame_idx > end_frame:
                break
                
            # Set position (to handle potential frame skipping issues)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            
            # Read the frame
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Failed to read frame at index {frame_idx}")
                break
            
            # Encode frame to base64
            frame_base64 = encode_image(frame)
            
            # Get frame timestamp
            frame_timestamp = frame_idx / video_info["fps"]
            
            # Add to frames list
            frames.append({
                "index": frame_idx,
                "timestamp_seconds": float(frame_timestamp),
                "timestamp_formatted": f"{int(frame_timestamp // 60):02d}:{int(frame_timestamp % 60):02d}.{int((frame_timestamp % 1) * 100):02d}",
                "image_base64": frame_base64
            })
        
        # Release the capture
        cap.release()
        
        # Clean up temporary file if needed
        if temp_path:
            try:
                os.remove(temp_path)
            except:
                pass
        
        return {
            "frames": frames,
            "frame_count": len(frames),
            "extraction_parameters": {
                "start_frame": start_frame,
                "end_frame": end_frame,
                "step": step,
                "max_frames": max_frames
            },
            "video_info": video_info
        }
        
    except Exception as e:
        logger.error(f"Error extracting video frames: {str(e)}")
        
        # Clean up temporary file if needed
        if temp_path:
            try:
                os.remove(temp_path)
            except:
                pass
                
        raise ValueError(f"Failed to extract video frames: {str(e)}")

def detect_motion_tool(
    frame1_base64: str,
    frame2_base64: str,
    threshold: int = 25,
    blur_size: int = 5,
    dilate_size: int = 5,
    min_area: int = 500,
    draw: bool = True,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> Dict[str, Any]:
    """
    Detect motion between two frames
    
    Args:
        frame1_base64: Base64 encoded first frame
        frame2_base64: Base64 encoded second frame
        threshold: Threshold for binary conversion
        blur_size: Kernel size for Gaussian blur
        dilate_size: Kernel size for dilation
        min_area: Minimum contour area to consider as motion
        draw: Whether to draw motion contours
        color: Color for drawing contours (BGR format)
        thickness: Thickness of contour lines
        
    Returns:
        Dict: Motion detection results and visualizations
    """
    try:
        # Decode frames
        frame1 = decode_image(frame1_base64)
        frame2 = decode_image(frame2_base64)
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blur1 = cv2.GaussianBlur(gray1, (blur_size, blur_size), 0)
        blur2 = cv2.GaussianBlur(gray2, (blur_size, blur_size), 0)
        
        # Calculate absolute difference
        frame_diff = cv2.absdiff(blur1, blur2)
        
        # Apply threshold
        _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Dilate to fill in holes
        kernel = np.ones((dilate_size, dilate_size), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and collect motion data
        motion_data = []
        
        # Copy frames for visualization
        diff_visualization = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        frame2_copy = frame2.copy()
        
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            if area >= min_area:
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                motion_data.append({
                    "index": i,
                    "area": float(area),
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "center": (int(x + w/2), int(y + h/2))
                })
                
                # Draw contour if requested
                if draw:
                    cv2.rectangle(frame2_copy, (x, y), (x+w, y+h), color, thickness)
                    cv2.drawContours(diff_visualization, [contour], -1, color, thickness)
        
        return {
            "original_frame1_base64": frame1_base64,
            "original_frame2_base64": frame2_base64,
            "diff_visualization_base64": encode_image(diff_visualization),
            "result_frame_base64": encode_image(frame2_copy) if draw else frame2_base64,
            "motion_detected": len(motion_data) > 0,
            "motion_count": len(motion_data),
            "motion_areas": motion_data,
            "total_motion_area": sum(m["area"] for m in motion_data),
            "parameters": {
                "threshold": threshold,
                "blur_size": blur_size,
                "dilate_size": dilate_size,
                "min_area": min_area
            }
        }
        
    except Exception as e:
        logger.error(f"Error detecting motion: {str(e)}")
        raise ValueError(f"Failed to detect motion: {str(e)}")

def track_object_tool(
    video_path: str,
    video_base64: Optional[str] = None,
    initial_bbox: List[int] = None,
    tracker_type: str = "kcf",
    start_frame: int = 0,
    max_frames: int = 50,
    frame_step: int = 1,
    extract_frames: bool = True,
    max_extract: int = 10
) -> Dict[str, Any]:
    """
    Track an object across video frames
    
    Args:
        video_path: Path to video file (can be None if video_base64 is provided)
        video_base64: Base64 encoded video string (optional)
        initial_bbox: Initial bounding box [x, y, width, height]
        tracker_type: Type of tracker ('kcf', 'csrt', 'mil', 'mosse', etc.)
        start_frame: Starting frame index (0-based)
        max_frames: Maximum number of frames to track
        frame_step: Step size (process every nth frame)
        extract_frames: Whether to extract frames with tracking visualization
        max_extract: Maximum number of frames to extract
        
    Returns:
        Dict: Tracking results and extracted frames
    """
    try:
        temp_path = None
        
        # Handle base64 input
        if video_base64 is not None:
            temp_path = decode_video_file(video_base64)
            video_path = temp_path
        
        # Open the video
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        # Get video info
        video_info = get_video_info(video_path)
        total_frames = video_info["frame_count"]
        
        # Validate parameters
        if start_frame < 0:
            start_frame = 0
        
        if frame_step < 1:
            frame_step = 1
        
        # Create tracker
        tracker_types = {
            "kcf": cv2.legacy.TrackerKCF_create if hasattr(cv2, 'legacy') else cv2.TrackerKCF_create,
            "csrt": cv2.legacy.TrackerCSRT_create if hasattr(cv2, 'legacy') else cv2.TrackerCSRT_create,
            "mil": cv2.legacy.TrackerMIL_create if hasattr(cv2, 'legacy') else cv2.TrackerMIL_create,
            "mosse": cv2.legacy.TrackerMOSSE_create if hasattr(cv2, 'legacy') else cv2.TrackerMOSSE_create,
            "medianflow": cv2.legacy.TrackerMedianFlow_create if hasattr(cv2, 'legacy') else cv2.TrackerMedianFlow_create,
            "tld": cv2.legacy.TrackerTLD_create if hasattr(cv2, 'legacy') else cv2.TrackerTLD_create,
            "boosting": cv2.legacy.TrackerBoosting_create if hasattr(cv2, 'legacy') else cv2.TrackerBoosting_create
        }
        
        if tracker_type.lower() not in tracker_types:
            raise ValueError(f"Unsupported tracker type: {tracker_type}. " + 
                           f"Supported types: {', '.join(tracker_types.keys())}")
        
        tracker_create = tracker_types[tracker_type.lower()]
        
        # Check if we need to select initial bbox from first frame
        if initial_bbox is None:
            # Set position to start_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            # Read the frame
            ret, frame = cap.read()
            
            if not ret:
                raise ValueError(f"Failed to read frame at index {start_frame}")
            
            # For API use, we'll need the user to provide the initial bbox
            # since we can't open interactive windows for selection
            raise ValueError("initial_bbox must be provided as [x, y, width, height]")
        
        # Validate initial bbox
        if len(initial_bbox) != 4:
            raise ValueError("initial_bbox must contain exactly 4 values: [x, y, width, height]")
        
        # Initialize tracker data
        tracking_data = []
        extracted_frames = []
        
        # Set position to start_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Read the first frame
        ret, frame = cap.read()
        
        if not ret:
            raise ValueError(f"Failed to read frame at index {start_frame}")
        
        # Initialize tracker
        tracker = tracker_create()
        bbox = tuple(initial_bbox)
        success = tracker.init(frame, bbox)
        
        if not success:
            raise ValueError(f"Failed to initialize tracker with the provided bounding box")
        
        # Add initial tracking data
        tracking_data.append({
            "frame": start_frame,
            "bbox": list(bbox),
            "success": success
        })
        
        # Extract first frame if requested
        if extract_frames:
            # Draw bounding box
            x, y, w, h = [int(v) for v in bbox]
            frame_vis = frame.copy()
            cv2.rectangle(frame_vis, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Add frame data
            frame_timestamp = start_frame / video_info["fps"]
            extracted_frames.append({
                "index": start_frame,
                "timestamp_seconds": float(frame_timestamp),
                "timestamp_formatted": f"{int(frame_timestamp // 60):02d}:{int(frame_timestamp % 60):02d}.{int((frame_timestamp % 1) * 100):02d}",
                "image_base64": encode_image(frame_vis)
            })
        
        # Process subsequent frames
        frame_count = 1
        extract_count = 1
        current_frame = start_frame + frame_step
        
        while frame_count < max_frames and current_frame < total_frames:
            # Set position to current frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            
            # Read the frame
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Update tracker
            success, bbox = tracker.update(frame)
            
            # Add tracking data
            tracking_data.append({
                "frame": current_frame,
                "bbox": list(bbox) if success else None,
                "success": success
            })
            
            # Extract frame if requested
            if extract_frames and extract_count < max_extract:
                frame_vis = frame.copy()
                
                if success:
                    # Draw bounding box
                    x, y, w, h = [int(v) for v in bbox]
                    cv2.rectangle(frame_vis, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Add frame data
                frame_timestamp = current_frame / video_info["fps"]
                extracted_frames.append({
                    "index": current_frame,
                    "timestamp_seconds": float(frame_timestamp),
                    "timestamp_formatted": f"{int(frame_timestamp // 60):02d}:{int(frame_timestamp % 60):02d}.{int((frame_timestamp % 1) * 100):02d}",
                    "tracking_success": success,
                    "image_base64": encode_image(frame_vis)
                })
                
                extract_count += 1
            
            # Increment counters
            frame_count += 1
            current_frame += frame_step
        
        # Release the capture
        cap.release()
        
        # Clean up temporary file if needed
        if temp_path:
            try:
                os.remove(temp_path)
            except:
                pass
        
        return {
            "tracking_data": tracking_data,
            "tracked_frame_count": len(tracking_data),
            "successful_tracks": sum(1 for t in tracking_data if t["success"]),
            "extracted_frames": extracted_frames,
            "extracted_frame_count": len(extracted_frames),
            "tracking_parameters": {
                "tracker_type": tracker_type,
                "initial_bbox": initial_bbox,
                "start_frame": start_frame,
                "max_frames": max_frames,
                "frame_step": frame_step
            },
            "video_info": video_info
        }
        
    except Exception as e:
        logger.error(f"Error tracking object: {str(e)}")
        
        # Clean up temporary file if needed
        if temp_path:
            try:
                os.remove(temp_path)
            except:
                pass
                
        raise ValueError(f"Failed to track object: {str(e)}")

def combine_frames_to_video_tool(
    frame_base64_list: List[str],
    output_path: str,
    fps: float = 30.0,
    width: Optional[int] = None,
    height: Optional[int] = None,
    fourcc: str = "mp4v"
) -> Dict[str, Any]:
    """
    Combine frames into a video file
    
    Args:
        frame_base64_list: List of base64 encoded frames
        output_path: Path to save the output video
        fps: Frames per second
        width: Output width (if None, use first frame's width)
        height: Output height (if None, use first frame's height)
        fourcc: FourCC code for output video codec
        
    Returns:
        Dict: Video creation results
    """
    try:
        if not frame_base64_list:
            raise ValueError("No frames provided")
        
        # Decode first frame to get dimensions if not specified
        first_frame = decode_image(frame_base64_list[0])
        
        if width is None or height is None:
            h, w = first_frame.shape[:2]
            width = width or w
            height = height or h
        
        # Create video writer
        fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
        out = cv2.VideoWriter(output_path, fourcc_code, fps, (width, height))
        
        if not out.isOpened():
            raise ValueError(f"Failed to create video writer: {output_path}")
        
        # Process each frame
        for i, frame_base64 in enumerate(frame_base64_list):
            # Decode frame
            frame = decode_image(frame_base64)
            
            # Resize if necessary
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))
            
            # Write frame
            out.write(frame)
        
        # Release writer
        out.release()
        
        return {
            "success": True,
            "output_path": output_path,
            "frame_count": len(frame_base64_list),
            "video_parameters": {
                "width": width,
                "height": height,
                "fps": fps,
                "fourcc": fourcc
            },
            "size_bytes": os.path.getsize(output_path) if os.path.exists(output_path) else None
        }
        
    except Exception as e:
        logger.error(f"Error combining frames to video: {str(e)}")
        raise ValueError(f"Failed to combine frames to video: {str(e)}")

def register_tools(mcp):
    """
    Register all video processing tools with the MCP server
    
    Args:
        mcp: The MCP server instance
    """
    # Register tool implementations
    mcp.tool(extract_video_frames_tool)
    mcp.tool(detect_motion_tool)
    mcp.tool(track_object_tool)
    mcp.tool(combine_frames_to_video_tool)
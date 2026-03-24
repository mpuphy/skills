#!/usr/bin/env python3
"""
Extract the last frame from a video file and save it as an image.
Uses FFmpeg (if available) or OpenCV as fallback.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import os


def has_ffmpeg() -> bool:
    """Check if FFmpeg is available."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_with_ffmpeg(video_path: str, output_path: str) -> str:
    """Extract last frame using FFmpeg."""
    cmd = [
        "ffmpeg",
        "-sseof", "-0.1",  # Seek to 0.1s before end (ensures we get a frame)
        "-i", video_path,
        "-vsync", "0",
        "-q:v", "2",       # High quality
        "-frames:v", "1",  # Extract only 1 frame
        "-y",              # Overwrite output
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return output_path


def extract_with_opencv(video_path: str, output_path: str) -> str:
    """Extract last frame using OpenCV."""
    try:
        import cv2
    except ImportError:
        raise RuntimeError(
            "OpenCV not installed. Install with: pip install opencv-python\n"
            "Or install FFmpeg: https://ffmpeg.org/download.html"
        )
    
    # Use cv2.imdecode for better Unicode support
    video_path = str(video_path)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        cap.release()
        raise RuntimeError(f"Could not determine frame count")
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        raise RuntimeError(f"Could not read last frame")
    
    # Use imencode for better Unicode support on Windows
    import numpy as np
    ext = Path(output_path).suffix.lower()
    if ext == '.png':
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
        result, buf = cv2.imencode('.png', frame, encode_param)
    elif ext in ['.jpg', '.jpeg']:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
        result, buf = cv2.imencode('.jpg', frame, encode_param)
    else:
        result, buf = cv2.imencode(ext, frame)
    
    if not result:
        raise RuntimeError(f"Could not encode image")
    
    # Write to file using binary mode
    with open(output_path, 'wb') as f:
        f.write(buf)
    
    if not os.path.exists(output_path):
        raise RuntimeError(f"Could not save image to: {output_path}")
    
    return output_path


def extract_last_frame(video_path: str, output_path: str = None, format: str = "png") -> str:
    """
    Extract the last frame from a video file.
    
    Args:
        video_path: Path to input video
        output_path: Path for output image (optional)
        format: Output format (png, jpg, jpeg, bmp, webp)
    
    Returns:
        Path to saved image
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    if output_path is None:
        # Use a simple default name to avoid encoding issues
        output_path = video_path.parent / f"last_frame.{format.lower()}"
    else:
        output_path = Path(output_path)
    
    # Convert to absolute path and resolve any issues
    output_path = output_path.resolve()
    
    # Try FFmpeg first (faster and more reliable)
    if has_ffmpeg():
        result = extract_with_ffmpeg(str(video_path), str(output_path))
    else:
        result = extract_with_opencv(str(video_path), str(output_path))
    
    # Verify file was created
    if not os.path.exists(result):
        raise RuntimeError(f"Output file was not created: {result}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract the last frame from a video file."
    )
    parser.add_argument("video", help="Input video file path")
    parser.add_argument("-o", "--output", help="Output image path")
    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpg", "jpeg", "bmp", "webp"],
        default="png",
        help="Output format (default: png)"
    )
    
    args = parser.parse_args()
    
    try:
        output = extract_last_frame(args.video, args.output, args.format)
        # Print absolute path for clarity
        print(f"Last frame saved to: {Path(output).resolve()}")
        print(f"File size: {os.path.getsize(output)} bytes")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

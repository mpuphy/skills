#!/usr/bin/env python3
"""
Extract last frame from video using pure Python + FFmpeg if available.
This script tries multiple methods.
"""

import subprocess
import sys
from pathlib import Path

def has_ffmpeg() -> bool:
    """Check if FFmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def extract_with_ffmpeg(video_path: str, output_path: str) -> str:
    """Extract last frame using FFmpeg."""
    cmd = [
        "ffmpeg",
        "-sseof", "-0.1",
        "-i", video_path,
        "-vsync", "0",
        "-q:v", "2",
        "-frames:v", "1",
        "-y",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return output_path

def extract_with_cv2(video_path: str, output_path: str) -> str:
    """Extract last frame using OpenCV."""
    import cv2
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        raise RuntimeError("Could not determine frame count")
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        raise RuntimeError("Could not read last frame")
    
    if not cv2.imwrite(output_path, frame):
        raise RuntimeError(f"Could not save image to: {output_path}")
    
    return output_path

def main():
    video_path = r"C:\Users\zsz\Downloads\jimeng-2026-02-14-1431-是张小凡，是林惊羽，场景参考 【东方神话锚点】 高动态、清晰、东方史诗感、无崩坏....mp4"
    output_path = r"C:\Users\zsz\Downloads\jimeng-last-frame.png"
    
    if not Path(video_path).exists():
        print(f"Error: Video not found: {video_path}")
        sys.exit(1)
    
    try:
        # Try FFmpeg first
        if has_ffmpeg():
            print("Using FFmpeg...")
            extract_with_ffmpeg(video_path, output_path)
        else:
            print("FFmpeg not found, trying OpenCV...")
            extract_with_cv2(video_path, output_path)
        
        print(f"Success! Last frame saved to: {output_path}")
        
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("\nPlease install one of the following:")
        print("  1. FFmpeg (recommended): https://ffmpeg.org/download.html")
        print("  2. OpenCV: pip install opencv-python")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

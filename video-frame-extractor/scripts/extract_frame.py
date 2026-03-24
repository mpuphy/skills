#!/usr/bin/env python3
"""
Extract any frame from a video file.
Supports extraction by timestamp, frame number, or position (first/last).
Uses FFmpeg (if available) or OpenCV as fallback.
"""

import argparse
import subprocess
import sys
import re
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


def parse_time(time_str: str) -> float:
    """Parse time string to seconds.
    
    Supports:
    - 30 or 30s -> 30 seconds
    - 1:30 or 01:30 -> 1 minute 30 seconds
    - 01:30:00 -> 1 hour 30 minutes
    - 90.5 -> 90.5 seconds
    """
    time_str = str(time_str).strip().lower()
    
    # Remove trailing 's' if present
    if time_str.endswith('s') and time_str[:-1].replace('.', '', 1).isdigit():
        time_str = time_str[:-1]
    
    # Try direct float conversion (seconds)
    try:
        return float(time_str)
    except ValueError:
        pass
    
    # Parse HH:MM:SS or MM:SS format
    parts = time_str.split(':')
    if len(parts) == 2:  # MM:SS
        return float(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:  # HH:MM:SS
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    
    raise ValueError(f"Cannot parse time format: {time_str}")


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS.ms"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    else:
        return f"{minutes:02d}:{secs:06.3f}"


def get_video_duration(video_path: str) -> float:
    """Get video duration in seconds using FFprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return None


def get_video_info_opencv(video_path: str) -> dict:
    """Get video info using OpenCV."""
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else None
        
        cap.release()
        return {
            'fps': fps,
            'total_frames': total_frames,
            'duration': duration
        }
    except:
        return None


def extract_with_ffmpeg(video_path: str, output_path: str, timestamp: float = None, frame_number: int = None) -> str:
    """Extract frame using FFmpeg."""
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-q:v", "2",       # High quality
        "-frames:v", "1",  # Extract only 1 frame
        "-y",              # Overwrite output
    ]
    
    # Add time/frame seeking
    if timestamp is not None:
        cmd.extend(["-ss", str(timestamp)])
    elif frame_number is not None:
        # Get fps first
        duration = get_video_duration(video_path)
        info = get_video_info_opencv(video_path)
        if info and info['fps'] > 0:
            timestamp = frame_number / info['fps']
            cmd.extend(["-ss", str(timestamp)])
        else:
            # Fallback: use frame number with select filter
            cmd.extend(["-vf", f"select=eq(n\\,{frame_number})"])
    
    cmd.append(output_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return output_path


def extract_with_opencv(video_path: str, output_path: str, timestamp: float = None, 
                        frame_number: int = None, position: str = None) -> str:
    """Extract frame using OpenCV."""
    try:
        import cv2
    except ImportError:
        raise RuntimeError(
            "OpenCV not installed. Install with: pip install opencv-python\n"
            "Or install FFmpeg: https://ffmpeg.org/download.html"
        )
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if total_frames <= 0:
        cap.release()
        raise RuntimeError(f"Could not determine frame count")
    
    # Determine target frame
    if position == "first":
        target_frame = 0
    elif position == "last":
        target_frame = total_frames - 1
    elif frame_number is not None:
        target_frame = min(max(0, frame_number), total_frames - 1)
    elif timestamp is not None:
        target_frame = min(max(0, int(timestamp * fps)), total_frames - 1)
    else:
        # Default to first frame
        target_frame = 0
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        raise RuntimeError(f"Could not read frame at position {target_frame}")
    
    # Use imencode for better Unicode support on Windows
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


def extract_frame(video_path: str, timestamp: float = None, frame_number: int = None,
                  position: str = None, output_path: str = None, format: str = "png") -> str:
    """
    Extract a frame from a video file.
    
    Args:
        video_path: Path to input video
        timestamp: Time in seconds (e.g., 90.5 for 1:30.5)
        frame_number: Frame number to extract (0-indexed)
        position: "first" or "last" for convenience
        output_path: Path for output image (optional)
        format: Output format (png, jpg, jpeg, bmp, webp)
    
    Returns:
        Path to saved image
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    # Generate default output name
    if output_path is None:
        # Include time/frame info in filename
        suffix = ""
        if position:
            suffix = f"_{position}"
        elif frame_number is not None:
            suffix = f"_frame{frame_number}"
        elif timestamp is not None:
            suffix = f"_t{timestamp:.2f}s"
        
        output_path = video_path.parent / f"{video_path.stem}{suffix}.{format.lower()}"
    else:
        output_path = Path(output_path)
    
    output_path = output_path.resolve()
    
    # Try FFmpeg first (faster and more reliable)
    if has_ffmpeg():
        result = extract_with_ffmpeg(str(video_path), str(output_path), timestamp, frame_number)
    else:
        result = extract_with_opencv(str(video_path), str(output_path), timestamp, frame_number, position)
    
    # Verify file was created
    if not os.path.exists(result):
        raise RuntimeError(f"Output file was not created: {result}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract any frame from a video file."
    )
    parser.add_argument("video", help="Input video file path")
    
    # Extraction options (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-t", "--time", help="Timestamp (e.g., 30, 1:30, 01:30:00)")
    group.add_argument("-n", "--frame", type=int, help="Frame number (0-indexed)")
    group.add_argument("--first", action="store_true", help="Extract first frame")
    group.add_argument("--last", action="store_true", help="Extract last frame")
    
    parser.add_argument("-o", "--output", help="Output image path")
    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpg", "jpeg", "bmp", "webp"],
        default="png",
        help="Output format (default: png)"
    )
    
    args = parser.parse_args()
    
    # Determine extraction method
    timestamp = None
    frame_number = None
    position = None
    
    if args.time:
        timestamp = parse_time(args.time)
    elif args.frame is not None:
        frame_number = args.frame
    elif args.first:
        position = "first"
    elif args.last:
        position = "last"
    else:
        # Default to first frame if no option specified
        position = "first"
    
    try:
        output = extract_frame(
            args.video,
            timestamp=timestamp,
            frame_number=frame_number,
            position=position,
            output_path=args.output,
            format=args.format
        )
        
        output_path = Path(output)
        print(f"Frame saved to: {output_path.resolve()}")
        print(f"File size: {os.path.getsize(output)} bytes")
        
        # Print what was extracted
        if timestamp is not None:
            print(f"Extracted at timestamp: {format_time(timestamp)}")
        elif frame_number is not None:
            print(f"Extracted frame number: {frame_number}")
        elif position:
            print(f"Extracted {position} frame")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract the last frame from a video file using only av (PyAV) library.
"""

import argparse
import sys
from pathlib import Path

def extract_last_frame(video_path: str, output_path: str = None, format: str = "png") -> str:
    """Extract the last frame from a video using PyAV."""
    try:
        import av
        from PIL import Image
    except ImportError as e:
        raise RuntimeError(
            f"Missing package: {e}\n"
            "Please run: pip install av pillow"
        )
    
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    print("Opening video...")
    
    container = av.open(str(video_path))
    
    # Get the video stream
    stream = container.streams.video[0]
    
    # Get total duration and frame rate
    duration = stream.duration
    time_base = stream.time_base
    
    if duration is None:
        # Fallback: iterate through all frames
        print("Scanning frames...")
        frames = list(container.decode(stream))
        if not frames:
            raise RuntimeError("No frames found in video")
        last_frame = frames[-1]
    else:
        # Seek to near the end
        end_time = int(duration * 0.99)  # Seek to 99% of duration
        container.seek(end_time, stream=stream)
        
        # Get the last frame
        frames = list(container.decode(stream))
        if not frames:
            raise RuntimeError("Could not decode frames")
        last_frame = frames[-1]
    
    container.close()
    
    # Convert to PIL Image
    img = last_frame.to_image()
    
    # Determine output path
    if output_path is None:
        output_path = video_path.with_suffix(f".{format.lower()}")
    else:
        output_path = Path(output_path)
    
    # Save
    img.save(output_path, format=format.upper() if format != "jpg" else "JPEG")
    
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Extract the last frame from a video file using PyAV."
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
        print(f"Last frame saved to: {output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

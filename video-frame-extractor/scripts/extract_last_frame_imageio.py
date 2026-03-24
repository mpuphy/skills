#!/usr/bin/env python3
"""
Extract the last frame from a video file using imageio (no OpenCV/FFmpeg required).
"""

import argparse
import sys
from pathlib import Path

def extract_last_frame(video_path: str, output_path: str = None, format: str = "png") -> str:
    """Extract the last frame from a video using imageio."""
    try:
        import imageio.v3 as iio
        from PIL import Image
    except ImportError:
        raise RuntimeError(
            "Required packages not installed. Run:\n"
            "  pip install imageio pillow imageio-ffmpeg"
        )
    
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Read all frames metadata to get the last one
    print("Reading video frames...")
    
    try:
        # Get frame count
        meta = iio.immeta(video_path, plugin="pyav")
        n_frames = meta.get('n_frames', None)
        
        if n_frames is None or n_frames == 0:
            # Alternative: read all frames
            frames = list(iio.imiter(video_path, plugin="pyav"))
            if not frames:
                raise RuntimeError("Could not read any frames from video")
            last_frame = frames[-1]
        else:
            # Read the last frame directly
            last_frame = iio.imread(video_path, index=n_frames - 1, plugin="pyav")
    except Exception as e:
        print(f"pyav plugin failed: {e}")
        print("Trying FFmpeg plugin...")
        # Fallback to FFmpeg plugin
        frames = list(iio.imiter(video_path, plugin="FFMPEG"))
        if not frames:
            raise RuntimeError("Could not read any frames from video")
        last_frame = frames[-1]
    
    # Determine output path
    if output_path is None:
        output_path = video_path.with_suffix(f".{format.lower()}")
    else:
        output_path = Path(output_path)
    
    # Convert to PIL Image and save
    if len(last_frame.shape) == 3 and last_frame.shape[2] == 3:
        # RGB to BGR conversion for imageio format
        img = Image.fromarray(last_frame)
    else:
        img = Image.fromarray(last_frame)
    
    img.save(output_path, format=format.upper())
    
    return str(output_path)


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
        print(f"Last frame saved to: {output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

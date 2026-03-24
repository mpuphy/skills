"""
Extract all frames from a video file.
"""
import cv2
import sys
import os
from pathlib import Path

def extract_all_frames(video_path, output_dir=None, format='png'):
    """
    Extract all frames from a video file.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save frames (default: same as video file)
        format: Image format (png, jpg)
    
    Returns:
        Path to output directory containing frames
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    
    # Set output directory
    if output_dir is None:
        output_dir = video_path.parent / "frames"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video info:")
    print(f"  Resolution: {width}x{height}")
    print(f"  Total frames: {total_frames}")
    print(f"  FPS: {fps:.2f}")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Output directory: {output_dir}")
    print("")
    
    # Extract frames
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        output_file = output_dir / f"{video_path.stem}_frame_{frame_count:04d}.{format}"
        cv2.imwrite(str(output_file), frame)
        saved_count += 1
        
        # Progress indicator
        if frame_count % 30 == 0 or frame_count == 1:
            print(f"  Progress: {frame_count}/{total_frames} frames...")
    
    cap.release()
    
    print(f"\n✅ Done! Extracted {saved_count} frames to:")
    print(f"   {output_dir}")
    
    return str(output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <video_file> [-o output_dir] [-f format]")
        sys.exit(1)
    
    video_file = sys.argv[1]
    output_dir = None
    format = 'png'
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '-f' and i + 1 < len(sys.argv):
            format = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    extract_all_frames(video_file, output_dir, format)

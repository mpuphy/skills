#!/usr/bin/env python3
"""
Extract last frame using imageio-ffmpeg which auto-downloads FFmpeg.
"""

import sys
from pathlib import Path

def main():
    video_path = Path(r"C:\Users\zsz\Downloads\jimeng-2026-02-14-1431-是张小凡，是林惊羽，场景参考 【东方神话锚点】 高动态、清晰、东方史诗感、无崩坏....mp4")
    output_path = Path(r"C:\Users\zsz\Downloads\jimeng-last-frame.png")
    
    if not video_path.exists():
        print(f"Error: Video not found: {video_path}")
        sys.exit(1)
    
    try:
        # imageio-ffmpeg will auto-download FFmpeg on first use
        import imageio_ffmpeg
        from PIL import Image
        import numpy as np
        
        print("Getting FFmpeg...")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"FFmpeg located: {ffmpeg_exe}")
        
        # Use imageio to read video
        import imageio.v3 as iio
        
        print("Reading video frames...")
        # Get metadata
        meta = iio.immeta(video_path, plugin="FFMPEG")
        n_frames = meta.get('n_frames', 0)
        
        if n_frames == 0:
            # Read all frames
            frames = list(iio.imiter(video_path, plugin="FFMPEG"))
            if not frames:
                raise RuntimeError("Could not read any frames")
            last_frame = frames[-1]
        else:
            # Read last frame directly
            last_frame = iio.imread(video_path, index=n_frames-1, plugin="FFMPEG")
        
        # Save as image
        img = Image.fromarray(last_frame)
        img.save(output_path)
        
        print(f"Success! Last frame saved to: {output_path}")
        
    except ImportError as e:
        print(f"Missing package: {e}")
        print("Please install: pip install imageio imageio-ffmpeg pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

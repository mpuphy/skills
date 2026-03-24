#!/usr/bin/env python3
"""
Download FFmpeg and extract last frame from video.
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
TEMP_DIR = Path(os.environ.get("TEMP", "/tmp")) / "ffmpeg_auto"

def download_file(url: str, dest: Path) -> bool:
    """Download a file with progress."""
    try:
        print(f"Downloading from {url}...")
        print("This may take a few minutes depending on your connection...")
        
        # Disable proxy for this request
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        urllib.request.install_opener(opener)
        
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded to {dest}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def find_ffmpeg_exe(extract_dir: Path) -> Path:
    """Find ffmpeg.exe in extracted directory."""
    for path in extract_dir.rglob("ffmpeg.exe"):
        return path
    return None

def get_ffmpeg() -> Path:
    """Get FFmpeg executable path, downloading if necessary."""
    ffmpeg_exe = TEMP_DIR / "ffmpeg.exe"
    
    if ffmpeg_exe.exists():
        print(f"Using cached FFmpeg: {ffmpeg_exe}")
        return ffmpeg_exe
    
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = TEMP_DIR / "ffmpeg.zip"
    
    if not download_file(FFMPEG_URL, zip_path):
        raise RuntimeError("Failed to download FFmpeg")
    
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(TEMP_DIR)
    
    # Find ffmpeg.exe
    ffmpeg_path = find_ffmpeg_exe(TEMP_DIR)
    if not ffmpeg_path:
        raise RuntimeError("Could not find ffmpeg.exe in extracted archive")
    
    # Copy to standard location
    import shutil
    shutil.copy2(ffmpeg_path, ffmpeg_exe)
    print(f"FFmpeg ready: {ffmpeg_exe}")
    
    return ffmpeg_exe

def extract_last_frame(video_path: str, output_path: str, ffmpeg_exe: Path) -> str:
    """Extract last frame using FFmpeg."""
    cmd = [
        str(ffmpeg_exe),
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

def main():
    video_path = r"C:\Users\zsz\Downloads\jimeng-2026-02-14-1431-是张小凡，是林惊羽，场景参考 【东方神话锚点】 高动态、清晰、东方史诗感、无崩坏....mp4"
    output_path = r"C:\Users\zsz\Downloads\jimeng-last-frame.png"
    
    if not Path(video_path).exists():
        print(f"Error: Video not found: {video_path}")
        sys.exit(1)
    
    try:
        print("Setting up FFmpeg...")
        ffmpeg_exe = get_ffmpeg()
        
        print("Extracting last frame...")
        extract_last_frame(video_path, output_path, ffmpeg_exe)
        
        print(f"Success! Last frame saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

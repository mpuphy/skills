#!/usr/bin/env python3
"""
Direct download FFmpeg from alternative sources and extract last frame.
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Alternative download sources
FFMPEG_SOURCES = [
    # 腾讯软件源
    "https://mirrors.cloud.tencent.com/ffmpeg/ffmpeg-master-latest-win64-gpl.zip",
    # 华为云
    "https://repo.huaweicloud.com/ffmpeg/ffmpeg-master-latest-win64-gpl.zip",
    # 原始源
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
]

TEMP_DIR = Path(os.environ.get("TEMP", "/tmp")) / "ffmpeg_auto"

def download_with_progress(url: str, dest: Path) -> bool:
    """Download file with progress bar."""
    try:
        print(f"Downloading from: {url}")
        
        # Create request with no proxy
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0')
        
        # Build opener without proxy
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        
        with opener.open(req, timeout=120) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            block_size = 8192
            
            with open(dest, 'wb') as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded // 1024 // 1024}MB / {total_size // 1024 // 1024}MB)", end='', flush=True)
            
            print()  # New line after progress
            return True
            
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def find_ffmpeg_exe(directory: Path) -> Path:
    """Find ffmpeg.exe in directory."""
    for path in directory.rglob("ffmpeg.exe"):
        return path
    return None

def get_ffmpeg() -> Path:
    """Get FFmpeg, downloading if necessary."""
    ffmpeg_exe = TEMP_DIR / "ffmpeg.exe"
    
    if ffmpeg_exe.exists():
        print(f"Using cached FFmpeg: {ffmpeg_exe}")
        return ffmpeg_exe
    
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = TEMP_DIR / "ffmpeg.zip"
    
    # Try each source
    for source in FFMPEG_SOURCES:
        if download_with_progress(source, zip_path):
            break
    else:
        raise RuntimeError("Failed to download FFmpeg from all sources")
    
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(TEMP_DIR)
    
    # Find and copy ffmpeg.exe
    ffmpeg_path = find_ffmpeg_exe(TEMP_DIR)
    if not ffmpeg_path:
        raise RuntimeError("Could not find ffmpeg.exe in archive")
    
    shutil.copy2(ffmpeg_path, ffmpeg_exe)
    print(f"FFmpeg ready: {ffmpeg_exe}")
    
    # Cleanup zip
    zip_path.unlink(missing_ok=True)
    
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
        print("Setting up FFmpeg (one-time setup)...")
        ffmpeg_exe = get_ffmpeg()
        
        print("Extracting last frame from video...")
        extract_last_frame(video_path, output_path, ffmpeg_exe)
        
        print(f"✓ Success! Last frame saved to: {output_path}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

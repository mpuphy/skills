---
name: video-frame-extractor
description: Extract and save frames from a video file at any timestamp or frame number. Use when the user wants to capture a specific frame, create thumbnails, or convert video moments to static images.
triggers:
  - "保存视频帧"
  - "提取视频帧"
  - "截取视频画面"
  - "视频转图片"
  - "取视频第"
  - "视频帧"
---

# Video Frame Extractor

Extract any frame from a video file by timestamp (e.g., 00:01:30) or frame number.

## Usage

### Extract by Timestamp

```bash
python scripts/extract_frame.py <video_file> -t 00:01:30
```

### Extract by Frame Number

```bash
python scripts/extract_frame.py <video_file> -n 150
```

### Extract First/Last Frame

```bash
# First frame
python scripts/extract_frame.py <video_file> --first

# Last frame
python scripts/extract_frame.py <video_file> --last
```

### Specify Output Path

```bash
python scripts/extract_frame.py <video_file> -t 00:02:00 -o screenshot.png
```

### Choose Format

```bash
python scripts/extract_frame.py <video_file> -t 30s -f jpg
```

Supported formats: `png` (default), `jpg`, `jpeg`, `bmp`, `webp`

## Time Format

Timestamps support multiple formats:
- `30` or `30s` - 30 seconds
- `1:30` or `01:30` - 1 minute 30 seconds
- `01:30:00` - 1 hour 30 minutes
- `90.5` - 90.5 seconds (decimal allowed)

## Requirements

**Option 1: FFmpeg (Recommended)**
- Download: https://ffmpeg.org/download.html
- Add to PATH or use full path

**Option 2: OpenCV (Fallback)**
- `pip install opencv-python`

## Supported Video Formats

Any format supported by FFmpeg/OpenCV:
- MP4, AVI, MKV, MOV, WMV, FLV, WebM, and more

## Python API

```python
from scripts.extract_frame import extract_frame

# Extract at specific timestamp (seconds)
output = extract_frame("video.mp4", timestamp=90.5)

# Extract specific frame number
output = extract_frame("video.mp4", frame_number=150)

# Extract first or last frame
output = extract_frame("video.mp4", position="first")
output = extract_frame("video.mp4", position="last")

# Specify output
output = extract_frame("video.mp4", timestamp=120, output_path="frame.png")
```

## How It Works

1. **FFmpeg mode (preferred)**: Seeks to the specified time/frame and extracts that frame directly. Fast and reliable for all formats.

2. **OpenCV mode (fallback)**: Opens the video, calculates frame position from timestamp or uses frame number directly, seeks, and saves. Pure Python solution.

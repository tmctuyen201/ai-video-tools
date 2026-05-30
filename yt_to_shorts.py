#!/usr/bin/env python3
"""
🎬 YT to Shorts — Crop/Resize YouTube videos to 9:16 vertical Shorts format.

Uses FFmpeg to intelligently crop landscape (16:9) videos to portrait (9:16)
format suitable for YouTube Shorts, TikTok, and Instagram Reels.

Usage:
    python yt_to_shorts.py input.mp4 --output shorts.mp4
    python yt_to_shorts.py input.mp4 --scale 1080x1920 --fps 30
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def get_video_info(input_path: str) -> dict:
    """Get video metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", input_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: Cannot read video file: {input_path}")
        sys.exit(1)

    import json
    data = json.loads(result.stdout)
    video_stream = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {
        "width": int(video_stream["width"]),
        "height": int(video_stream["height"]),
        "duration": float(data["format"].get("duration", 0)),
        "fps": eval(video_stream.get("r_frame_rate", "30/1")),
    }


def crop_to_shorts(input_path: str, output_path: str, target_w: int = 1080,
                   target_h: int = 1920, crf: int = 23, preset: str = "medium"):
    """Crop and resize video to 9:16 vertical format centered."""
    info = get_video_info(input_path)
    src_w, src_h = info["width"], info["height"]

    # Calculate crop dimensions to maintain 9:16 from source
    target_ratio = target_w / target_h  # 0.5625
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider — crop horizontally
        crop_h = src_h
        crop_w = int(src_h * target_ratio)
    else:
        # Source is taller — crop vertically
        crop_w = src_w
        crop_h = int(src_w / target_ratio)

    # Build FFmpeg filter: crop center, then scale to target
    vf = (
        f"crop={crop_w}:{crop_h}:(iw-{crop_w})/2:(ih-{crop_h})/2,"
        f"scale={target_w}:{target_h}:flags=lanczos"
    )

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", str(crf), "-preset", preset,
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]

    print(f"📐 Source: {src_w}x{src_h} → Target: {target_w}x{target_h}")
    print(f"🔄 Cropping to {crop_w}x{crop_h}, then scaling...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Done! Output: {output_path} ({size_mb:.1f} MB)")
    else:
        print(f"❌ FFmpeg error:\n{result.stderr[-500:]}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Convert landscape videos to 9:16 Shorts format",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file path (default: <input>_shorts.mp4)")
    parser.add_argument("-s", "--scale", default="1080x1920",
                        help="Target resolution WxH (default: 1080x1920)")
    parser.add_argument("--crf", type=int, default=23,
                        help="Video quality (0-51, lower=better, default: 23)")
    parser.add_argument("--preset", default="medium",
                        choices=["ultrafast", "fast", "medium", "slow"],
                        help="Encoding speed preset (default: medium)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"❌ File not found: {args.input}")
        sys.exit(1)

    # Parse scale
    w, h = map(int, args.scale.split("x"))

    # Default output name
    if args.output is None:
        stem = Path(args.input).stem
        args.output = f"{stem}_shorts.mp4"

    crop_to_shorts(args.input, args.output, w, h, args.crf, args.preset)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
📐 Batch Resize — Resize videos for all social media platforms at once.

Generates optimally-sized versions of your video for YouTube, TikTok,
Instagram, Twitter, and LinkedIn in a single run.

Usage:
    python batch_resize.py input.mp4 --output-dir ./output/
    python batch_resize.py input.mp4 --platforms youtube tiktok instagram
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


# Platform presets: (name, width, height, max_fps, description)
PLATFORMS = {
    "youtube": {
        "width": 1920, "height": 1080, "label": "YouTube (16:9)",
        "crf": 23, "maxrate": "8M"
    },
    "youtube_shorts": {
        "width": 1080, "height": 1920, "label": "YouTube Shorts (9:16)",
        "crf": 23, "maxrate": "8M"
    },
    "tiktok": {
        "width": 1080, "height": 1920, "label": "TikTok (9:16)",
        "crf": 26, "maxrate": "6M"
    },
    "instagram_reel": {
        "width": 1080, "height": 1920, "label": "Instagram Reel (9:16)",
        "crf": 24, "maxrate": "6M"
    },
    "instagram_post": {
        "width": 1080, "height": 1080, "label": "Instagram Post (1:1)",
        "crf": 24, "maxrate": "5M"
    },
    "twitter": {
        "width": 1280, "height": 720, "label": "Twitter (16:9)",
        "crf": 26, "maxrate": "5M"
    },
    "linkedin": {
        "width": 1920, "height": 1080, "label": "LinkedIn (16:9)",
        "crf": 23, "maxrate": "8M"
    },
}


def resize_video(input_path: str, output_path: str, width: int, height: int,
                 crf: int = 23, maxrate: str = "8M"):
    """Resize a single video to specified dimensions."""
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
               f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264", "-crf", str(crf),
        "-maxrate", maxrate, "-bufsize", "2M",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        return True, size_mb
    return False, result.stderr[-200:]


def batch_resize(input_path: str, output_dir: str, platform_names: list):
    """Resize video for multiple platforms."""
    os.makedirs(output_dir, exist_ok=True)
    stem = Path(input_path).stem

    # Get input video info
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
           "-of", "csv=p=0", input_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = float(result.stdout.strip()) if result.stdout.strip() else 0

    print(f"🎬 Input: {input_path}")
    print(f"⏱️  Duration: {duration:.1f}s")
    print(f"📂 Output: {output_dir}")
    print(f"🎯 Platforms: {', '.join(platform_names)}")
    print("=" * 50)

    total = len(platform_names)
    done = 0

    for platform_name in platform_names:
        if platform_name not in PLATFORMS:
            print(f"⚠️  Unknown platform: {platform_name}")
            continue

        p = PLATFORMS[platform_name]
        output_path = os.path.join(output_dir, f"{stem}_{platform_name}.mp4")

        print(f"\n🔄 [{done+1}/{total}] {p['label']} → {p['width']}x{p['height']}")
        success, result = resize_video(
            input_path, output_path, p["width"], p["height"], p["crf"], p["maxrate"]
        )

        if success:
            print(f"   ✅ Done — {result:.1f} MB")
        else:
            print(f"   ❌ Failed: {result}")
        done += 1

    print(f"\n{'=' * 50}")
    print(f"🏁 Complete! {done}/{total} platforms processed.")
    print(f"📂 Files saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="📐 Batch resize videos for all social media platforms"
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-d", "--output-dir", default="./resized",
                        help="Output directory (default: ./resized)")
    parser.add_argument("--platforms", nargs="+", default=list(PLATFORMS.keys()),
                        choices=PLATFORMS.keys(),
                        help="Target platforms (default: all)")
    parser.add_argument("--list", action="store_true", help="List all platforms")

    args = parser.parse_args()

    if args.list:
        print("\n📺 Available platforms:")
        for name, p in PLATFORMS.items():
            print(f"   {name:20s} — {p['label']} ({p['width']}x{p['height']})")
        return

    if not os.path.isfile(args.input):
        print(f"❌ File not found: {args.input}")
        sys.exit(1)

    batch_resize(args.input, args.output_dir, args.platforms)


if __name__ == "__main__":
    main()

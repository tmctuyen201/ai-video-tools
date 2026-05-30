#!/usr/bin/env python3
"""
💬 Auto Caption — Add AI-powered subtitles to videos using OpenAI Whisper.

Automatically transcribes speech and burns subtitles into the video using FFmpeg.
Supports multiple languages and Whisper model sizes.

Usage:
    python auto_caption.py input.mp4
    python auto_caption.py input.mp4 --model medium --language en
    python auto_caption.py input.mp4 --srt-only --output subs.srt
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

try:
    import whisper
except ImportError:
    print("❌ Install Whisper: pip install openai-whisper")
    sys.exit(1)


def transcribe(input_path: str, model_name: str = "base",
               language: str = None) -> dict:
    """Transcribe audio using Whisper."""
    print(f"🧠 Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)

    print(f"🎤 Transcribing: {input_path}")
    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(input_path, **options)
    print(f"✅ Detected language: {result.get('language', 'unknown')}")
    return result


def generate_srt(result: dict, output_path: str) -> str:
    """Convert Whisper result to SRT subtitle format."""
    srt_lines = []
    for i, segment in enumerate(result["segments"], 1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n")

    srt_content = "\n".join(srt_lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    print(f"📝 SRT saved: {output_path}")
    return output_path


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def burn_subtitles(input_path: str, srt_path: str, output_path: str,
                   font_size: int = 24, font_color: str = "white",
                   outline_color: str = "black", outline_width: int = 2):
    """Burn SRT subtitles into video using FFmpeg."""
    # Escape path for FFmpeg subtitle filter
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
    style = (
        f"FontSize={font_size},"
        f"PrimaryColour=&H{color_to_hex(font_color)},"
        f"OutlineColour=&H{color_to_hex(outline_color)},"
        f"Outline={outline_width},"
        f"Alignment=2,MarginV=40"
    )

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"subtitles={srt_escaped}:force_style='{style}'",
        "-c:v", "libx264", "-crf", "23", "-preset", "medium",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path
    ]

    print(f"🔥 Burning subtitles into video...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Done! Output: {output_path} ({size_mb:.1f} MB)")
    else:
        print(f"❌ FFmpeg error:\n{result.stderr[-500:]}")
        sys.exit(1)


def color_to_hex(color_name: str) -> str:
    """Convert common color names to ASS hex format (BGR)."""
    colors = {
        "white": "FFFFFF", "yellow": "00FFFF", "red": "0000FF",
        "blue": "FF0000", "green": "00FF00", "cyan": "FFFF00",
    }
    return colors.get(color_name.lower(), "FFFFFF")


def main():
    parser = argparse.ArgumentParser(
        description="💬 Add AI-powered captions to videos using Whisper"
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-o", "--output", default=None, help="Output video file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code (e.g., 'en', 'vi', 'ja')")
    parser.add_argument("--srt-only", action="store_true",
                        help="Only generate SRT file, don't burn into video")
    parser.add_argument("--font-size", type=int, default=24,
                        help="Subtitle font size (default: 24)")
    parser.add_argument("--font-color", default="white",
                        help="Subtitle color (default: white)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"❌ File not found: {args.input}")
        sys.exit(1)

    # Transcribe
    result = transcribe(args.input, args.model, args.language)

    # Generate SRT
    stem = Path(args.input).stem
    srt_path = f"{stem}.srt"
    generate_srt(result, srt_path)

    if args.srt_only:
        print("🏁 SRT-only mode complete.")
        return

    # Burn subtitles
    if args.output is None:
        args.output = f"{stem}_captioned.mp4"
    burn_subtitles(args.input, srt_path, args.output, args.font_size, args.font_color)


if __name__ == "__main__":
    main()

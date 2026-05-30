"""auto-caption: Add AI-powered captions to videos using Whisper."""
import click
from rich.console import Console
from pathlib import Path
import subprocess
import json
import sys
import tempfile

console = Console()

STYLES = {
    "tiktok": {
        "font": "Montserrat-Bold",
        "fontsize": 48,
        "fontcolor": "white",
        "borderw": 3,
        "bordercolor": "black",
        "position": "bottom",
    },
    "youtube": {
        "font": "Arial",
        "fontsize": 36,
        "fontcolor": "white",
        "borderw": 2,
        "bordercolor": "black",
        "position": "bottom",
    },
    "instagram": {
        "font": "Helvetica-Bold",
        "fontsize": 42,
        "fontcolor": "white",
        "borderw": 3,
        "bordercolor": "#333333",
        "position": "center",
    },
    "netflix": {
        "font": "Arial-Bold",
        "fontsize": 40,
        "fontcolor": "white",
        "borderw": 0,
        "shadow": True,
        "position": "bottom",
    },
}


def transcribe_video(video_path: str, model: str = "base") -> list:
    """Transcribe video using Whisper."""
    console.print(f"[bold blue]Transcribing with Whisper ({model} model)...[/]")
    try:
        import whisper
        model_obj = whisper.load_model(model)
        result = model_obj.transcribe(video_path, word_timestamps=True)
        
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
                "words": seg.get("words", []),
            })
        return segments
    except ImportError:
        console.print("[red]Error: Install whisper: pip install openai-whisper[/]")
        sys.exit(1)


def generate_srt(segments: list, output_path: str):
    """Generate SRT subtitle file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text']}\n\n")


def format_time(seconds: float) -> str:
    """Format seconds to SRT time format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_ass(segments: list, output_path: str, style: str = "tiktok",
                 font: str = None, fontsize: int = None, color: str = None):
    """Generate ASS subtitle file with styling."""
    s = STYLES.get(style, STYLES["tiktok"])
    
    font_name = font or s["font"]
    size = fontsize or s["fontsize"]
    font_color = color or s.get("fontcolor", "white")
    
    # Color mapping
    color_map = {
        "white": "&H00FFFFFF",
        "yellow": "&H0000FFFF",
        "red": "&H000000FF",
        "green": "&H0000FF00",
    }
    ass_color = color_map.get(font_color, "&H00FFFFFF")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("[Script Info]\n")
        f.write("Title: Auto Caption\n")
        f.write("ScriptType: v4.00+\n")
        f.write("PlayResX: 1920\nPlayResY: 1080\n\n")
        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write(f"Style: Default,{font_name},{size},{ass_color},1,1,3,0,2,10,10,40,1\n\n")
        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        for seg in segments:
            start = format_ass_time(seg["start"])
            end = format_ass_time(seg["end"])
            text = seg["text"].replace("\n", " ")
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")


def format_ass_time(seconds: float) -> str:
    """Format seconds to ASS time format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def burn_subtitles(video_path: str, sub_path: str, output_path: str):
    """Burn subtitles into video using ffmpeg."""
    console.print("[bold green]Burning captions into video...[/]")
    cmd = f'ffmpeg -y -i "{video_path}" -vf "subtitles={sub_path}" -c:a copy "{output_path}"
    subprocess.run(cmd, shell=True, check=True)


@click.command()
@click.argument("video_path")
@click.option("--model", "-m", default="base", help="Whisper model: tiny, base, small, medium, large")
@click.option("--style", "-s", default="tiktok", type=click.Choice(list(STYLES.keys())),
              help="Caption style")
@click.option("--font", "-f", default=None, help="Override font name")
@click.option("--font-size", default=None, type=int, help="Override font size")
@click.option("--color", "-c", default=None, help="Font color: white, yellow, red, green")
@click.option("--output", "-o", default=None, help="Output path")
@click.option("--srt-only", is_flag=True, help="Export SRT file only (no burn)")
def cli(video_path: str, model: str, style: str, font: str,
        font_size: int, color: str, output: str, srt_only: bool):
    """Add AI-powered captions to videos using Whisper.
    
    Examples:
        auto-caption video.mp4 --style tiktok
        auto-caption video.mp4 --model small --color yellow
        auto-caption video.mp4 --srt-only
    """
    path = Path(video_path)
    if not path.exists():
        console.print(f"[red]Error: File not found: {video_path}[/]")
        sys.exit(1)
    
    # Transcribe
    segments = transcribe_video(str(path), model)
    console.print(f"[green]Found {len(segments)} segments[/]")
    
    # Generate subtitle file
    with tempfile.NamedTemporaryFile(suffix=".ass", delete=False, mode="w") as f:
        ass_path = f.name
    generate_ass(segments, ass_path, style, font, font_size, color)
    
    # Also save SRT
    srt_path = str(path.with_suffix(".srt"))
    generate_srt(segments, srt_path)
    console.print(f"[green]SRT saved:[/] {srt_path}")
    
    if srt_only:
        return
    
    # Burn captions
    out = output or str(path.with_stem(path.stem + "_captioned"))
    burn_subtitles(str(path), ass_path, out)
    console.print(f"[bold green]✅ Output:[/] {out}")


if __name__ == "__main__":
    cli()

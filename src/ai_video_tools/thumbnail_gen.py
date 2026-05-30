"""thumbnail-gen: Generate thumbnails with text overlays."""
import click
from rich.console import Console
from pathlib import Path
import subprocess
import sys
import json

console = Console()

STYLES = {
    "bold": {
        "font": "Impact",
        "fontsize": 80,
        "fontcolor": "white",
        "stroke_color": "black",
        "stroke_width": 4,
    },
    "clean": {
        "font": "Arial-Bold",
        "fontsize": 60,
        "fontcolor": "white",
        "stroke_color": "black",
        "stroke_width": 2,
    },
    "neon": {
        "font": "Impact",
        "fontsize": 72,
        "fontcolor": "#00FF88",
        "stroke_color": "#003322",
        "stroke_width": 3,
    },
    "minimal": {
        "font": "Helvetica",
        "fontsize": 48,
        "fontcolor": "white",
        "stroke_color": "none",
        "stroke_width": 0,
    },
}


def extract_best_frame(video_path: str, output_path: str) -> str:
    """Extract the frame with highest contrast from video."""
    console.print("[bold blue]Finding best frame...[/]")
    
    # Get video duration
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "json", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = float(json.loads(result.stdout)["format"]["duration"])
    
    # Sample 5 frames and pick middle one
    sample_time = duration * 0.3
    cmd = f'ffmpeg -y -ss {sample_time} -i "{video_path}" -vframes 1 -q:v 2 "{output_path}"
    subprocess.run(cmd, shell=True, check=True, capture_output=True)
    
    return output_path


def add_text_overlay(image_path: str, text: str, output_path: str,
                     style: str = "bold", emoji: str = None,
                     width: int = 1280, height: int = 720):
    """Add text overlay to image using ffmpeg."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.open(image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)
        
        s = STYLES.get(style, STYLES["bold"])
        
        # Try to load font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s["fontsize"])
        except (OSError, IOError):
            font = ImageFont.load_default()
        
        # Add emoji prefix if specified
        display_text = f"{emoji} {text}" if emoji else text
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (width - text_w) // 2
        y = (height - text_h) // 2
        
        # Draw stroke
        if s["stroke_width"] > 0:
            for dx in range(-s["stroke_width"], s["stroke_width"] + 1):
                for dy in range(-s["stroke_width"], s["stroke_width"] + 1):
                    draw.text((x + dx, y + dy), display_text, font=font, fill=s["stroke_color"])
        
        # Draw text
        draw.text((x, y), display_text, font=font, fill=s["fontcolor"])
        
        img.save(output_path, quality=95)
        console.print(f"[bold green]✅ Thumbnail saved:[/] {output_path}")
        
    except ImportError:
        console.print("[red]Error: Install Pillow: pip install Pillow[/]")
        sys.exit(1)


@click.command()
@click.argument("video_path", required=False)
@click.option("--bg", default=None, help="Background image path (instead of video frame)")
@click.option("--text", "-t", required=True, help="Text to overlay")
@click.option("--style", "-s", default="bold", type=click.Choice(list(STYLES.keys())))
@click.option("--emoji", "-e", default=None, help="Emoji prefix")
@click.option("--output", "-o", default="thumbnail.png", help="Output path")
@click.option("--width", default=1280, help="Thumbnail width")
@click.option("--height", default=720, help="Thumbnail height")
def cli(video_path: str, bg: str, text: str, style: str, emoji: str,
        output: str, width: int, height: int):
    """Generate thumbnails with text overlays.
    
    Examples:
        thumbnail-gen video.mp4 --text "EPIC VIDEO" --style bold
        thumbnail-gen --bg photo.png --text "10X GROWTH" --emoji 🔥
    """
    if bg:
        source = bg
    elif video_path:
        source = str(Path(output).with_suffix(".tmp.png"))
        extract_best_frame(video_path, source)
    else:
        console.print("[red]Error: Provide video path or --bg image[/]")
        sys.exit(1)
    
    add_text_overlay(source, text, output, style, emoji, width, height)


if __name__ == "__main__":
    cli()

"""batch-resize: Batch resize videos for all platforms."""
import click
from rich.console import Console
from rich.table import Table
from pathlib import Path
import subprocess
import sys
import os

console = Console()

PLATFORMS = {
    "tiktok": {"width": 1080, "height": 1920, "max_duration": 180, "fps": 30},
    "instagram": {"width": 1080, "height": 1920, "max_duration": 90, "fps": 30},
    "youtube_shorts": {"width": 1080, "height": 1920, "max_duration": 60, "fps": 30},
    "youtube": {"width": 1920, "height": 1080, "max_duration": None, "fps": 30},
    "twitter": {"width": 1280, "height": 720, "max_duration": 140, "fps": 30},
}

QUALITY_PRESETS = {
    "low": {"crf": 28, "preset": "fast"},
    "medium": {"crf": 23, "preset": "medium"},
    "high": {"crf": 18, "preset": "slow"},
}


def get_video_files(directory: str) -> list:
    """Get all video files in directory."""
    exts = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv"}
    path = Path(directory)
    if path.is_file():
        return [str(path)]
    return [str(f) for f in path.rglob("*") if f.suffix.lower() in exts]


def resize_video(input_path: str, output_path: str, platform: str,
                 quality: str = "medium"):
    """Resize video for specific platform."""
    p = PLATFORMS[platform]
    q = QUALITY_PRESETS[quality]
    
    w, h = p["width"], p["height"]
    max_dur = f"-t {p['max_duration']}" if p["max_duration"] else ""
    
    vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
    
    cmd = (
        f'ffmpeg -y -i "{input_path}" '
        f'-vf "{vf}" '
        f'-r {p["fps"]} '
        f'-c:v libx264 -crf {q["crf"]} -preset {q["preset"]} '
        f'-c:a aac -b:a 128k '
        f'{max_dur} '
        f'"{output_path}"'
    )
    
    subprocess.run(cmd, shell=True, check=True, capture_output=True)


@click.command()
@click.argument("input_path")
@click.option("--platforms", "-p", default="all",
              help="Comma-separated: tiktok,instagram,youtube_shorts,youtube,twitter or 'all'")
@click.option("--output", "-o", default="export/", help="Output directory")
@click.option("--quality", "-q", default="medium",
              type=click.Choice(["low", "medium", "high"]))
def cli(input_path: str, platforms: str, output: str, quality: str):
    """Batch resize videos for all social platforms.
    
    Examples:
        batch-resize video.mp4 --platforms tiktok,instagram
        batch-resize ./videos/ --platforms all --quality high
    """
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if platforms == "all":
        platform_list = list(PLATFORMS.keys())
    else:
        platform_list = [p.strip() for p in platforms.split(",")]
    
    # Validate platforms
    for p in platform_list:
        if p not in PLATFORMS:
            console.print(f"[red]Unknown platform: {p}[/]")
            console.print(f"Available: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
    
    videos = get_video_files(input_path)
    if not videos:
        console.print("[red]No video files found[/]")
        sys.exit(1)
    
    # Show preview table
    table = Table(title="Batch Resize Plan")
    table.add_column("Video", style="cyan")
    table.add_column("Platform", style="green")
    table.add_column("Resolution", style="yellow")
    table.add_column("Quality", style="magenta")
    
    for video in videos:
        for platform in platform_list:
            p = PLATFORMS[platform]
            table.add_row(
                Path(video).name,
                platform,
                f"{p['width']}x{p['height']}",
                quality
            )
    
    console.print(table)
    
    # Process
    total = len(videos) * len(platform_list)
    done = 0
    
    for video in videos:
        video_name = Path(video).stem
        for platform in platform_list:
            out_path = str(output_dir / f"{video_name}_{platform}.mp4")
            console.print(f"[blue]Processing:[/] {video_name} → {platform}")
            try:
                resize_video(video, out_path, platform, quality)
                done += 1
                console.print(f"[green]  ✅ Done ({done}/{total})[/]")
            except Exception as e:
                console.print(f"[red]  ❌ Error: {e}[/]")
    
    console.print(f"\n[bold green]🎉 Complete! {done}/{total} videos processed[/]")
    console.print(f"[green]Output directory:[/] {output_dir}")


if __name__ == "__main__":
    cli()

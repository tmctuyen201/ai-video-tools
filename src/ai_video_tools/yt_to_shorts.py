"""yt-to-shorts: Convert YouTube videos to Shorts format."""
import click
from rich.console import Console
from pathlib import Path
import subprocess
import json
import sys

console = Console()


def get_video_info(path: str) -> dict:
    """Get video metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-show_format",
        path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def detect_face_center(video_path: str) -> tuple:
    """Detect the center of faces in video for smart cropping."""
    try:
        import cv2
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if not ret:
            return (0.5, 0.5)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        cap.release()
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            h_frame, w_frame = frame.shape[:2]
            return ((x + w / 2) / w_frame, (y + h / 2) / h_frame)
    except ImportError:
        pass
    return (0.5, 0.5)


def download_video(url: str, output: str) -> str:
    """Download YouTube video using yt-dlp."""
    console.print(f"[bold blue]Downloading:[/] {url}")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", output,
        "--merge-output-format", "mp4",
        url
    ]
    subprocess.run(cmd, check=True)
    return output


def convert_to_shorts(input_path: str, output_path: str, crop: str = "center",\                      max_duration: int = 59, add_captions: bool = False) -> str:
    """Convert video to 9:16 Shorts format."""
    info = get_video_info(input_path)
    streams = info.get("streams", [])
    video_stream = next((s for s in streams if s["codec_type"] == "video"), None)
    
    if not video_stream:
        console.print("[red]Error: No video stream found[/]")
        sys.exit(1)
    
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    
    # Calculate crop for 9:16 (target: 1080x1920)
    target_ratio = 9 / 16
    current_ratio = width / height
    
    if crop == "smart":
        cx, cy = detect_face_center(input_path)
    else:
        cx, cy = 0.5, 0.5
    
    if current_ratio > target_ratio:
        new_w = int(height * target_ratio)
        x_offset = int((width - new_w) * cx)
        x_offset = max(0, min(x_offset, width - new_w))
        crop_filter = f"crop={new_w}:{height}:{x_offset}:0"
    else:
        new_h = int(width / target_ratio)
        y_offset = int((height - new_h) * cy)
        y_offset = max(0, min(y_offset, height - new_h))
        crop_filter = f"crop={width}:{new_h}:0:{y_offset}"
    
    # Scale to 1080x1920
    scale_filter = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
    
    # Trim duration
    trim = f"-t {max_duration}" if max_duration else ""
    
    # Build ffmpeg command
    vf = f"{crop_filter},{scale_filter}"
    cmd = f'ffmpeg -y -i "{input_path}" -vf "{vf}" {trim} -c:a aac -b:a 128k "{output_path}"
    
    console.print(f"[bold green]Converting to Shorts format...[/]")
    subprocess.run(cmd, shell=True, check=True)
    console.print(f"[bold green]✅ Output:[/] {output_path}")
    return output_path


@click.command()
@click.argument("input_path")
@click.option("--output", "-o", default="shorts/", help="Output directory")
@click.option("--crop", default="center", type=click.Choice(["center", "smart"]),
              help="Crop mode: center or smart (face detection)")
@click.option("--max-duration", default=59, help="Max duration in seconds")
@click.option("--add-captions", is_flag=True, help="Add auto-captions")
def cli(input_path: str, output: str, crop: str, max_duration: int, add_captions: bool):
    """Convert YouTube videos to Shorts format.
    
    Examples:
        yt-to-shorts https://youtube.com/watch?v=xxxxx
        yt-to-shorts video.mp4 --crop smart --add-captions
    """
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download if URL
    if input_path.startswith("http"):
        downloaded = str(output_dir / "downloaded.mp4")
        input_path = download_video(input_path, downloaded)
    
    output_path = str(output_dir / "shorts.mp4")
    convert_to_shorts(input_path, output_path, crop, max_duration, add_captions)


if __name__ == "__main__":
    cli()

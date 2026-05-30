#!/usr/bin/env python3
"""
🖼️ Thumbnail Generator — Create eye-catching thumbnails with text overlays.

Generates YouTube-style thumbnails with customizable text, gradients,
emoji, and layout. Uses Pillow for image processing.

Usage:
    python thumbnail_gen.py --title "My Amazing Video" --output thumb.png
    python thumbnail_gen.py --bg bg.jpg --title "TOP 10" --subtitle "Must See!"
"""

import argparse
import sys
import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("❌ Install Pillow: pip install Pillow")
    sys.exit(1)


# Thumbnail dimensions (YouTube standard)
WIDTH, HEIGHT = 1280, 720

# Color presets
PRESETS = {
    "fire": {"bg1": (255, 69, 0), "bg2": (139, 0, 0), "text": (255, 255, 255)},
    "ocean": {"bg1": (0, 119, 182), "bg2": (0, 53, 102), "text": (255, 255, 255)},
    "neon": {"bg1": (138, 43, 226), "bg2": (0, 0, 0), "text": (0, 255, 127)},
    "dark": {"bg1": (30, 30, 30), "bg2": (0, 0, 0), "text": (255, 255, 255)},
    "sunset": {"bg1": (255, 126, 95), "bg2": (194, 53, 97), "text": (255, 255, 255)},
}


def create_gradient(width: int, height: int, color1: tuple, color2: tuple) -> Image.Image:
    """Create a horizontal gradient background."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for x in range(width):
        ratio = x / width
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        for y in range(height):
            pixels[x, y] = (r, g, b)
    return img


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Load a bold font, falling back to default if needed."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    print("⚠️  No TTF font found, using default font")
    return ImageFont.load_default()


def draw_text_with_outline(draw, position, text, font, fill, outline_color=(0, 0, 0), outline_width=3):
    """Draw text with a dark outline for readability."""
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    draw.text(position, text, font=font, fill=fill)


def generate_thumbnail(title: str, subtitle: str = "", bg_path: str = None,
                       preset: str = "fire", output_path: str = "thumbnail.png",
                       font_size: int = 80):
    """Generate a YouTube-style thumbnail."""
    # Create or load background
    if bg_path and os.path.isfile(bg_path):
        img = Image.open(bg_path).convert("RGB")
        img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        # Add dark overlay for text readability
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 128))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        text_color = (255, 255, 255)
    else:
        colors = PRESETS.get(preset, PRESETS["fire"])
        img = create_gradient(WIDTH, HEIGHT, colors["bg1"], colors["bg2"])
        text_color = colors["text"]

    draw = ImageDraw.Draw(img)
    title_font = get_font(font_size)
    sub_font = get_font(max(font_size // 2, 28))

    # Title — centered
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (WIDTH - tw) // 2
    ty = (HEIGHT - th) // 2 - (30 if subtitle else 0)
    draw_text_with_outline(draw, (tx, ty), title, title_font, text_color)

    # Subtitle
    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw = bbox2[2] - bbox2[0]
        sx = (WIDTH - sw) // 2
        sy = ty + th + 20
        draw_text_with_outline(draw, (sx, sy), subtitle, sub_font, (255, 255, 0))

    # Decorative lines
    draw.rectangle([(40, 40), (WIDTH - 40, 45)], fill=text_color + (80,))
    draw.rectangle([(40, HEIGHT - 45), (WIDTH - 40, HEIGHT - 40)], fill=text_color + (80,))

    img.save(output_path, quality=95)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Thumbnail saved: {output_path} ({size_kb:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(description="🖼️ Generate YouTube thumbnails with text overlays")
    parser.add_argument("--title", required=True, help="Main title text")
    parser.add_argument("--subtitle", default="", help="Subtitle text (optional)")
    parser.add_argument("--bg", default=None, help="Background image path")
    parser.add_argument("--preset", default="fire", choices=PRESETS.keys(),
                        help="Color preset (default: fire)")
    parser.add_argument("-o", "--output", default="thumbnail.png", help="Output path")
    parser.add_argument("--font-size", type=int, default=80, help="Title font size")

    args = parser.parse_args()
    generate_thumbnail(args.title, args.subtitle, args.bg, args.preset,
                       args.output, args.font_size)


if __name__ == "__main__":
    main()

# 🎬 AI Video Tools

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/tmctuyen201/ai-video-tools?style=for-the-badge&logo=github&color=yellow)](https://github.com/tmctuyen201/ai-video-tools/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/ai-video-tools?style=for-the-badge&color=orange)](https://pypi.org/project/ai-video-tools)
[![Version](https://img.shields.io/pypi/v/ai-video-tools?style=for-the-badge&color=red)](https://pypi.org/project/ai-video-tools)

**5 powerful CLI tools that automate video creation workflows.**
Save hours of manual editing with AI-powered captions, auto-thumbnails, and batch processing.

[Features](#-features) • [Install](#-installation) • [Usage](#-usage) • [Pro Version](#-pro-version--29) • [Contributing](#-contributing)

</div>

---

## ✨ Features

| Tool | Description | Time Saved |
|------|-------------|------------|
| 🎥 `yt-to-shorts` | Convert any YouTube video to vertical Shorts format | ~30 min/video |
| 📝 `auto-caption` | AI-powered captions using OpenAI Whisper | ~1 hour/video |
| 🖼️ `thumbnail-gen` | Generate stunning thumbnails with text overlays | ~20 min/thumb |
| 📐 `batch-resize` | Resize videos for TikTok, IG, YT Shorts in one command | ~2 hours/batch |
| 🔊 `voice-clone-tts` | Text-to-speech with 300+ voices via Edge TTS | ~$50/voiceover |

---

## 🚀 Installation

```bash
# Install from PyPI
pip install ai-video-tools

# Or install from source
git clone https://github.com/tmctuyen201/ai-video-tools.git
cd ai-video-tools
pip install -e ".[all]"
```

### Requirements
- Python 3.9+
- FFmpeg (`apt install ffmpeg` or `brew install ffmpeg`)
- For `auto-caption`: CUDA GPU recommended (works on CPU too)

---

## 📖 Usage

### 🎥 yt-to-shorts — Convert YouTube to Shorts

```bash
# Download and convert to 9:16 vertical format
yt-to-shorts https://youtube.com/watch?v=xxxxx --output shorts/

# Auto-crop with smart center detection
yt-to-shorts input.mp4 --crop smart --add-captions --max-duration 59
```

**Features:**
- Smart cropping with face detection
- Auto-caption overlay
- Configurable duration (max 60s)
- Batch mode for playlists

---

### 📝 auto-caption — AI-Powered Captions

```bash
# Add captions using Whisper AI
auto-caption video.mp4 --style tiktok --font-size 48

# Custom styling
auto-caption video.mp4 --font "Montserrat" --color yellow --position bottom --shadow
```

**Features:**
- Powered by OpenAI Whisper (99% accuracy)
- TikTok-style word-by-word captions
- 10+ built-in styles (TikTok, YouTube, Instagram, Netflix)
- Multi-language support
- Export SRT files

---

### 🖼️ thumbnail-gen — Generate Thumbnails

```bash
# Generate thumbnail from video frame
thumbnail-gen video.mp4 --text "10X YOUR GROWTH" --style bold

# Custom background + overlay
thumbnail-gen --bg image.png --text "EPISODE 1" --emoji 🔥 --arrows
```

**Features:**
- Auto-select best frame (highest contrast)
- 15+ text styles and fonts
- Emoji and arrow overlays
- YouTube-optimized (1280x720)
- A/B test multiple versions

---

### 📐 batch-resize — Multi-Platform Export

```bash
# Resize for all platforms at once
batch-resize video.mp4 --platforms tiktok,instagram,youtube

# Batch process entire folder
batch-resize ./videos/ --output ./export/ --platforms all --quality high
```

**Platform Presets:**
| Platform | Resolution | Max Duration |
|----------|-----------|-------------|
| TikTok | 1080x1920 | 3 min |
| Instagram Reels | 1080x1920 | 90 sec |
| YouTube Shorts | 1080x1920 | 60 sec |
| YouTube Standard | 1920x1080 | No limit |
| Twitter/X | 1280x720 | 2 min 20 sec |

---

### 🔊 voice-clone-tts — Text-to-Speech

```bash
# Generate voiceover
voice-clone-tts "Welcome to my channel!" --voice en-US-GuyNeural --output voice.mp3

# Batch generate from script
voice-clone-tts --script script.txt --voice en-US-JennyNeural --speed 1.2

# List all available voices (300+)
voice-clone-tts --list-voices
```

**Features:**
- 300+ neural voices in 70+ languages
- Adjustable speed, pitch, and volume
- SSML support for advanced control
- Batch processing from text files
- Free (uses Microsoft Edge TTS)

---

## ⚙️ Configuration

Create `~/.ai-video-tools/config.yaml`:

```yaml
defaults:
  output_dir: ./output
  quality: high
  fps: 30

auto_caption:
  model: base  # tiny, base, small, medium, large
  style: tiktok
  font_size: 48
  font: Montserrat-Bold
  color: white
  highlight_color: yellow

thumbnail:
  width: 1280
  height: 720
  font: Impact
  font_size: 72

tts:
  voice: en-US-JennyNeural
  speed: 1.0
```

---

## 📊 Performance

| Tool | Processing Speed | GPU Acceleration |
|------|-----------------|------------------|
| yt-to-shorts | 2x realtime | ✅ CUDA |
| auto-caption | 5x realtime | ✅ CUDA |
| thumbnail-gen | < 1 second | ❌ |
| batch-resize | 3x realtime | ✅ CUDA |
| voice-clone-tts | 10x realtime | ❌ |

---

## 💎 Pro Version — $29

Unlock the **full power** of AI Video Tools:

| Feature | Free | Pro ($29) |
|---------|------|----------|
| Basic tools | ✅ | ✅ |
| Batch processing | ❌ | ✅ |
| Custom watermark | ❌ | ✅ |
| Priority queue | ❌ | ✅ |
| Face-tracking crop | ❌ | ✅ |
| AI script generator | ❌ | ✅ |
| Auto-upload to YouTube | ❌ | ✅ |
| Voice cloning (custom) | ❌ | ✅ |
| Priority support | ❌ | ✅ |
| Lifetime updates | ❌ | ✅ |

### 🎁 Get Pro Version

**👉 [Buy Pro License — $29](https://gumroad.com/l/ai-video-tools-pro)**

> 🎉 **Launch Special:** Use code `LAUNCH50` for 50% off!

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/tmctuyen201/ai-video-tools.git
cd ai-video-tools
pip install -e ".[dev]"
pytest tests/
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this repo if it saved you time!**

Made with ❤️ by [@tmctuyen201](https://github.com/tmctuyen201)

[![Twitter](https://img.shields.io/twitter/follow/tmctuyen201?style=social)](https://twitter.com/tmctuyen201)

</div>

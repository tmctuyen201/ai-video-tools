# 🎬 AI Video Tools

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/version-1.0.0-orange?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/github/stars/tmctuyen201/ai-video-tools?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/badge/FFmpeg-required-red?style=for-the-badge&logo=ffmpeg" alt="FFmpeg">
</p>

> 🚀 A powerful collection of AI-powered video tools for content creators. Automate captions, thumbnails, resizing, and more — all from the command line.

---

## ✨ Features

| Tool | Description | Command |
|------|-------------|---------|
| 🎥 **YT to Shorts** | Crop/resize YouTube videos to 9:16 Shorts format | `python yt_to_shorts.py` |
| 💬 **Auto Caption** | AI-powered captions using OpenAI Whisper | `python auto_caption.py` |
| 🖼️ **Thumbnail Gen** | Generate thumbnails with text overlays | `python thumbnail_gen.py` |
| 📐 **Batch Resize** | Resize videos for all social platforms | `python batch_resize.py` |
| 🔊 **Voice TTS** | Text-to-speech with Microsoft Edge TTS | `python voice_tts.py` |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/tmctuyen201/ai-video-tools.git
cd ai-video-tools

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (required)
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows - download from https://ffmpeg.org/download.html
```

---

## 🚀 Quick Start

### 🎥 Convert YouTube Video to Shorts
```bash
python yt_to_shorts.py input_video.mp4 --output shorts_output.mp4
```

### 💬 Add AI Captions
```bash
python auto_caption.py input_video.mp4 --model base --language en
```

### 🖼️ Generate Thumbnail
```bash
python thumbnail_gen.py --image bg.jpg --title "My Video" --output thumb.png
```

### 📐 Batch Resize for All Platforms
```bash
python batch_resize.py input_video.mp4 --output-dir ./resized/
```

### 🔊 Text to Speech
```bash
python voice_tts.py "Hello world" --output speech.mp3 --voice en-US-AriaNeural
```

---

## 📖 Detailed Usage

Each tool includes built-in help:
```bash
python yt_to_shorts.py --help
python auto_caption.py --help
python thumbnail_gen.py --help
python batch_resize.py --help
python voice_tts.py --help
```

---

## 🛠️ Makefile Commands

```bash
make install     # Install all dependencies
make test        # Run tests
make clean       # Clean generated files
make help        # Show all available commands
```

---

## ⭐ Pro Version — $29

<p align="center">
  <img src="https://img.shields.io/badge/🔓_Pro_Version-$29-gold?style=for-the-badge&logo=stripe&logoColor=white" alt="Pro Version">
</p>

Unlock the **full power** of AI Video Tools with the Pro version:

- 🤖 **AI Script Writer** — Generate video scripts with GPT-4
- 🎨 **Advanced Thumbnails** — AI background removal & style transfer
- 📊 **Batch Processing** — Process hundreds of videos at once
- 🔄 **Auto Upload** — Direct upload to YouTube, TikTok, Instagram
- 🎵 **AI Music** — Generate background music for your videos
- 📈 **Analytics** — Track performance across platforms
- 🆕 **Priority Updates** — Get new features first

> 💳 **One-time payment. Lifetime access. No subscription.**
>
> 👉 [Get Pro Version](https://gumroad.com/l/ai-video-tools-pro) — Use code `LAUNCH50` for 50% off!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/tmctuyen201">tmctuyen201</a>
</p>

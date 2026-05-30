from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="ai-video-tools",
    version="1.0.0",
    author="tmctuyen201",
    author_email="tmctuyen201@gmail.com",
    description="5 powerful CLI tools for video creators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tmctuyen201/ai-video-tools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "yt-dlp>=2024.1.1",
        "openai-whisper>=20231117",
        "Pillow>=10.0",
        "edge-tts>=6.1",
        "opencv-python>=4.8",
        "ffmpeg-python>=0.2.0",
        "pyyaml>=6.0",
        "tqdm>=4.65",
    ],
    extras_require={
        "gpu": ["torch>=2.0"],
        "dev": ["pytest>=7.0", "black", "ruff"],
    },
    entry_points={
        "console_scripts": [
            "yt-to-shorts=ai_video_tools.yt_to_shorts:cli",
            "auto-caption=ai_video_tools.auto_caption:cli",
            "thumbnail-gen=ai_video_tools.thumbnail_gen:cli",
            "batch-resize=ai_video_tools.batch_resize:cli",
            "voice-clone-tts=ai_video_tools.voice_clone_tts:cli",
        ],
    },
)
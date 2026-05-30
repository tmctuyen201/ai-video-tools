#!/usr/bin/env python3
"""
🔊 Voice TTS — Text-to-speech using Microsoft Edge TTS.

Generates high-quality speech audio from text using Microsoft's neural
TTS voices. Supports 300+ voices in 70+ languages.

Usage:
    python voice_tts.py "Hello, welcome to my channel!"
    python voice_tts.py "Xin chào" --voice vi-VN-HoaiMyNeural -o hello.mp3
    python voice_tts.py --list-voices  # Show all available voices
"""

import argparse
import asyncio
import sys
import os

try:
    import edge_tts
except ImportError:
    print("❌ Install edge-tts: pip install edge-tts")
    sys.exit(1)


# Popular voices by language
POPULAR_VOICES = {
    "en-US": "en-US-AriaNeural",
    "en-GB": "en-GB-SoniaNeural",
    "vi-VN": "vi-VN-HoaiMyNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "ko-KR": "ko-KR-SunHiNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "fr-FR": "fr-FR-DeniseNeural",
    "de-DE": "de-DE-KatjaNeural",
    "es-ES": "es-ES-ElviraNeural",
    "pt-BR": "pt-BR-FranciscaNeural",
    "th-TH": "th-TH-PremwadeeNeural",
    "id-ID": "id-ID-GadisNeural",
}


async def list_voices():
    """List all available Edge TTS voices."""
    voices = await edge_tts.list_voices()
    print(f"\n🎤 Available voices ({len(voices)} total):\n")
    print(f"{'Voice ID':<40} {'Language':<10} {'Gender':<8}")
    print("-" * 60)
    for v in sorted(voices, key=lambda x: x["ShortName"]):
        print(f"{v['ShortName']:<40} {v['Locale']:<10} {v['Gender']:<8}")
    print(f"\n💡 Use: python voice_tts.py \"text\" --voice <VoiceID>")


async def text_to_speech(text: str, voice: str = "en-US-AriaNeural",
                         output_path: str = "output.mp3",
                         rate: str = "+0%", volume: str = "+0%",
                         pitch: str = "+0Hz"):
    """Convert text to speech and save to file."""
    print(f"🔊 Generating speech...")
    print(f"   Voice: {voice}")
    print(f"   Text: \"{text[:80]}{'...' if len(text) > 80 else ''}\"")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch
    )

    await communicate.save(output_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Saved: {output_path} ({size_kb:.0f} KB)")


async def text_to_speech_with_subtitles(text: str, voice: str,
                                         output_path: str, srt_path: str):
    """Generate speech with synchronized SRT subtitles."""
    print(f"🔊 Generating speech with subtitles...")
    communicate = edge_tts.Communicate(text=text, voice=voice)

    submaker = edge_tts.SubMaker()
    audio_data = b""

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
        elif chunk["type"] == "WordBoundary":
            submaker.create_sub(
                (chunk["offset"], chunk["duration"]),
                chunk["text"]
            )

    with open(output_path, "wb") as f:
        f.write(audio_data)

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(submaker.generate_subs())

    print(f"✅ Audio: {output_path}")
    print(f"📝 Subtitles: {srt_path}")


def main():
    parser = argparse.ArgumentParser(
        description="🔊 Text-to-speech using Microsoft Edge TTS"
    )
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("-o", "--output", default="output.mp3",
                        help="Output audio file (default: output.mp3)")
    parser.add_argument("--voice", default="en-US-AriaNeural",
                        help="Voice ID (default: en-US-AriaNeural)")
    parser.add_argument("--rate", default="+0%",
                        help="Speech rate, e.g. '+20%%' or '-10%%'")
    parser.add_argument("--volume", default="+0%",
                        help="Volume adjustment, e.g. '+50%%'")
    parser.add_argument("--pitch", default="+0Hz",
                        help="Pitch adjustment, e.g. '+10Hz'")
    parser.add_argument("--subtitles", action="store_true",
                        help="Also generate SRT subtitle file")
    parser.add_argument("--list-voices", action="store_true",
                        help="List all available voices")

    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(list_voices())
        return

    if not args.text:
        print("❌ Please provide text to convert.")
        print("   Usage: python voice_tts.py \"Hello world\"")
        sys.exit(1)

    if args.subtitles:
        srt_path = Path(args.output).stem + ".srt"
        asyncio.run(text_to_speech_with_subtitles(
            args.text, args.voice, args.output, srt_path
        ))
    else:
        asyncio.run(text_to_speech(
            args.text, args.voice, args.output,
            args.rate, args.volume, args.pitch
        ))


if __name__ == "__main__":
    from pathlib import Path
    main()

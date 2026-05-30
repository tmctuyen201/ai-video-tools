"""voice-clone-tts: Text-to-speech with Edge TTS."""
import click
from rich.console import Console
from pathlib import Path
import asyncio
import sys

console = Console()


def get_voices() -> list:
    """Get all available Edge TTS voices."""
    import edge_tts
    voices = asyncio.get_event_loop().run_until_complete(edge_tts.list_voices())
    return voices


def generate_speech(text: str, voice: str, output_path: str,
                    rate: str = "+0%", volume: str = "+0%"):
    """Generate speech from text using Edge TTS."""
    import edge_tts
    
    async def _generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
        await communicate.save(output_path)
    
    asyncio.get_event_loop().run_until_complete(_generate())


def list_voices_table(filter_lang: str = None):
    """Display available voices in a table."""
    from rich.table import Table
    
    voices = get_voices()
    table = Table(title="Available Edge TTS Voices")
    table.add_column("Voice Name", style="cyan")
    table.add_column("Language", style="green")
    table.add_column("Gender", style="yellow")
    
    for v in voices:
        lang = v["Locale"]
        if filter_lang and not lang.startswith(filter_lang):
            continue
        table.add_row(v["ShortName"], lang, v["Gender"])
    
    console.print(table)
    console.print(f"\n[green]Total: {len(voices)} voices[/]")


@click.command()
@click.argument("text", required=False)
@click.option("--voice", "-v", default="en-US-JennyNeural", help="Voice name")
@click.option("--output", "-o", default="output.mp3", help="Output file path")
@click.option("--speed", "-s", default=1.0, type=float, help="Speed multiplier (0.5-2.0)")
@click.option("--volume", default=1.0, type=float, help="Volume multiplier (0.0-2.0)")
@click.option("--script", default=None, help="Read text from file")
@click.option("--list-voices", "list_v", is_flag=True, help="List all available voices")
@click.option("--lang", default=None, help="Filter voices by language (e.g., en, vi, ja)")
def cli(text: str, voice: str, output: str, speed: float,
        volume: float, script: str, list_v: bool, lang: str):
    """Text-to-speech with 300+ voices via Edge TTS.
    
    Examples:
        voice-clone-tts "Hello world!" --voice en-US-GuyNeural
        voice-clone-tts --script script.txt --voice vi-VN-HoaiMyNeural
        voice-clone-tts --list-voices --lang en
    """
    if list_v:
        list_voices_table(lang)
        return
    
    # Get text
    if script:
        script_path = Path(script)
        if not script_path.exists():
            console.print(f"[red]Error: Script file not found: {script}[/]")
            sys.exit(1)
        text = script_path.read_text(encoding="utf-8")
    elif not text:
        console.print("[red]Error: Provide text or --script file[/]")
        sys.exit(1)
    
    # Convert speed to Edge TTS rate format
    rate = int((speed - 1) * 100)
    rate_str = f"+{rate}%" if rate >= 0 else f"{rate}%"
    vol = int((volume - 1) * 100)
    vol_str = f"+{vol}%" if vol >= 0 else f"{vol}%"
    
    console.print(f"[bold blue]Generating speech...[/]")
    console.print(f"  Voice: {voice}")
    console.print(f"  Speed: {speed}x ({rate_str})")
    console.print(f"  Output: {output}")
    
    generate_speech(text, voice, output, rate_str, vol_str)
    console.print(f"[bold green]✅ Saved:[/] {output}")


if __name__ == "__main__":
    cli()

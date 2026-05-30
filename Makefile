.PHONY: install clean test help shorts caption thumb resize tts

PYTHON ?= python3
PIP ?= pip3

## help: Show available commands
help:
	@echo "🎬 AI Video Tools — Available Commands:"
	@echo ""
	@echo "  make install    Install all dependencies"
	@echo "  make clean      Remove generated files"
	@echo "  make test       Run basic tests"
	@echo ""
	@echo "  make shorts INPUT=file.mp4    Convert to 9:16 Shorts"
	@echo "  make caption INPUT=file.mp4   Add AI captions"
	@echo "  make thumb TITLE='text'       Generate thumbnail"
	@echo "  make resize INPUT=file.mp4    Batch resize for platforms"
	@echo "  make tts TEXT='Hello'         Text to speech"

## install: Install all Python dependencies
install:
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed!"
	@echo "⚠️  Make sure FFmpeg is installed on your system."

## clean: Remove generated files
clean:
	rm -f *_shorts.mp4 *_captioned.mp4
	rm -f *.srt
	rm -f thumbnail.png output.mp3
	rm -rf resized/
	rm -rf __pycache__/
	@echo "🧹 Cleaned!"

## test: Run basic sanity tests
test:
	$(PYTHON) -c "from PIL import Image; print('✅ Pillow OK')"
	$(PYTHON) -c "import edge_tts; print('✅ Edge TTS OK')"
	@which ffmpeg > /dev/null && echo "✅ FFmpeg OK" || echo "❌ FFmpeg not found"
	@echo "🏁 Tests complete!"

## shorts: Convert video to Shorts format
shorts:
	$(PYTHON) yt_to_shorts.py $(INPUT) -o $(basename $(INPUT))_shorts.mp4

## caption: Add AI captions to video
caption:
	$(PYTHON) auto_caption.py $(INPUT)

## thumb: Generate thumbnail
thumb:
	$(PYTHON) thumbnail_gen.py --title "$(TITLE)" --subtitle "$(SUB)"

## resize: Batch resize for all platforms
resize:
	$(PYTHON) batch_resize.py $(INPUT)

## tts: Text to speech
tts:
	$(PYTHON) voice_tts.py "$(TEXT)"

## voices: List available TTS voices
voices:
	$(PYTHON) voice_tts.py --list-voices

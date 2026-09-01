"""
Transcribes the voiceover into an .srt caption file using OpenAI's Whisper,
running fully locally and free (no API key, no per-use cost).
"""
import whisper

def generate_captions(audio_path: str, output_path: str = "output/captions.srt") -> str:
    model = whisper.load_model("base")  # "tiny" is faster/lower quality, "small" is better/slower
    result = model.transcribe(audio_path, word_timestamps=False)

    def format_timestamp(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")

    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], start=1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text'].strip()}\n\n")

    return output_path


if __name__ == "__main__":
    path = generate_captions("output/voice.mp3")
    print(f"Saved captions to {path}")

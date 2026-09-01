"""
Combines a background clip + voiceover + burned-in captions into a final
vertical (1080x1920) short using ffmpeg via subprocess. Requires ffmpeg
installed and on PATH.
"""
import subprocess
import os

def get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())

def assemble_video(
    background_path: str = "assets/background.mp4",
    voice_path: str = "output/voice.mp3",
    captions_path: str = "output/captions.srt",
    output_path: str = "output/short.mp4",
) -> str:
    if not os.path.exists(background_path):
        raise FileNotFoundError(
            f"Missing {background_path} — add a royalty-free vertical background clip there."
        )

    duration = get_audio_duration(voice_path)

    # Escape path for ffmpeg's subtitles filter on Windows/paths with special chars
    captions_escaped = captions_path.replace("\\", "/").replace(":", "\\:")

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", background_path,   # loop background to cover duration
        "-i", voice_path,
        "-t", str(duration),
        "-vf",
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"subtitles='{captions_escaped}':force_style='FontSize=16,PrimaryColour=&HFFFFFF&,Bold=1'",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-c:a", "aac",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True)
    return output_path


if __name__ == "__main__":
    path = assemble_video()
    print(f"Saved final short to {path}")

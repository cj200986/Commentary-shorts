"""
Runs the full pipeline: topic -> script -> voice -> captions -> video -> (optional) upload.

Usage:
    python main.py              # builds the short, does not upload
    python main.py --upload     # builds the short and uploads to YouTube (needs OAuth setup)
"""
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

from fetch_topic import fetch_trending_topic
from generate_script import generate_script
from generate_voice import generate_voice
from generate_captions import generate_captions
from assemble_video import assemble_video

def run(upload: bool = False):
    os.makedirs("output", exist_ok=True)

    print("1/5 Fetching trending topic...")
    topic = fetch_trending_topic()
    print(f"    -> {topic}")

    print("2/5 Generating script...")
    script = generate_script(topic)
    print(f"    -> {script}\n")

    print("3/5 Generating voiceover...")
    voice_path = generate_voice(script)

    print("4/5 Generating captions...")
    captions_path = generate_captions(voice_path)

    print("5/5 Assembling final video...")
    timestamp = int(time.time())
    output_path = f"output/short_{timestamp}.mp4"
    assemble_video(voice_path=voice_path, captions_path=captions_path, output_path=output_path)
    print(f"\nDone. Final short saved to: {output_path}")

    if upload:
        from upload_youtube import upload_short
        upload_short(
            video_path=output_path,
            title=topic[:95],
            description=f"AI commentary short on: {topic}",
            privacy_status="private",  # flip to "public" once you trust the output
        )

if __name__ == "__main__":
    run(upload="--upload" in sys.argv)

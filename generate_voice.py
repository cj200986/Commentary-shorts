"""
Converts a script into an MP3 voiceover using gTTS (free, no API key required).

Swap this file out later for ElevenLabs or another paid TTS API once you
have revenue and want a less robotic voice — keep the same function signature
(generate_voice(script, output_path)) and nothing else in the pipeline needs
to change.
"""
from gtts import gTTS

def generate_voice(script: str, output_path: str = "output/voice.mp3") -> str:
    tts = gTTS(text=script, lang="en", slow=False)
    tts.save(output_path)
    return output_path


if __name__ == "__main__":
    sample = "This is a test of the free text to speech voice."
    path = generate_voice(sample)
    print(f"Saved voiceover to {path}")

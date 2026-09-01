# AI Commentary Shorts — Automated Pipeline (Free Stack)

Pulls a trending topic → writes a script with an LLM → generates a voiceover →
adds captions → assembles a vertical short → (optionally) uploads to YouTube.
Runs locally or for free on a schedule via GitHub Actions.

## Pipeline
```
fetch_topic.py      → picks a trending Reddit post title as the topic
generate_script.py  → Claude/OpenAI API writes a 30-60s commentary script
generate_voice.py   → gTTS turns the script into an MP3 voiceover (free, no API key)
generate_captions.py→ Whisper (local, free) transcribes the voiceover into an .srt
assemble_video.py   → ffmpeg combines a background clip + voiceover + burned-in captions
upload_youtube.py   → uploads the finished short to YouTube (optional, needs OAuth)
main.py             → runs all steps in order
```

## 1. Install locally
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
You also need **ffmpeg** installed and on your PATH:
- Mac: `brew install ffmpeg`
- Windows: download from ffmpeg.org, add to PATH
- Linux: `sudo apt install ffmpeg`

## 2. Add your API key
Copy `.env.example` to `.env` and add ONE of:
- `ANTHROPIC_API_KEY=...` (get free trial credit at console.anthropic.com)
- `OPENAI_API_KEY=...`

This is the only paid-ish piece — script generation costs a fraction of a cent
per short. Everything else (gTTS, Whisper, ffmpeg) is free.

## 3. Add a background clip
Drop a royalty-free vertical video (from Pexels/Pixabay, or your own screen
recording) into `assets/background.mp4`. The pipeline loops/crops it to fit
your voiceover length automatically.

## 4. Run it
```bash
python main.py
```
Output lands in `output/short_<timestamp>.mp4`, ready to upload manually,
or automatically if you set up YouTube upload (see below).

## 5. (Optional) Automate uploads to YouTube
1. Go to Google Cloud Console → create a project → enable "YouTube Data API v3"
2. Create OAuth credentials (Desktop app) → download as `client_secret.json`
   into the project root
3. Run `python upload_youtube.py` once locally — it'll open a browser to
   authorize and save a `token.json` for future automated runs
4. From then on, `main.py --upload` will upload automatically

## 6. Run it on a free schedule (no server needed)
This repo includes `.github/workflows/daily.yml`, which runs the whole
pipeline once a day for free on GitHub Actions.

1. Push this folder to a new GitHub repo
2. Go to repo Settings → Secrets and variables → Actions → add:
   - `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`)
3. Commit `token.json` and `client_secret.json` as secrets too if you want
   auto-upload (or just let it build the video and download it from the
   Action's build artifacts each day)
4. Done — it runs daily on GitHub's free compute, no laptop required

## Notes
- gTTS voice quality is robotic-but-fine to start (same as the "stupid guy"
  origin story). Swap in ElevenLabs later once you have revenue — just
  replace `generate_voice.py`'s function body.
- Always use content you have rights to react to/comment on (screen
  recordings of trending clips for commentary is generally fair use, but
  don't just re-upload someone else's video wholesale).
- Start with `main.py` running manually a few times before trusting the
  scheduled auto-upload — check script quality and video output first.

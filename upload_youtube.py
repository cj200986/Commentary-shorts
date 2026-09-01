"""
Uploads the finished short to YouTube using the YouTube Data API v3.

One-time setup:
1. Google Cloud Console -> new project -> enable "YouTube Data API v3"
2. Create OAuth client credentials (Desktop app type) -> download as
   client_secret.json into this project's root folder
3. Run this file once locally: `python upload_youtube.py`
   A browser window opens for you to authorize your channel.
   This saves token.json so future runs don't need the browser step.
"""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        with open("token.json", "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)

def upload_short(
    video_path: str,
    title: str,
    description: str = "",
    tags: list = None,
    privacy_status: str = "private",  # switch to "public" once you trust the pipeline
) -> str:
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags or [],
            "categoryId": "24",  # Entertainment
        },
        "status": {"privacyStatus": privacy_status},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"Uploaded: https://youtube.com/watch?v={video_id}")
    return video_id


if __name__ == "__main__":
    upload_short(
        video_path="output/short.mp4",
        title="Test upload from automated pipeline",
        description="Automated AI commentary short.",
        privacy_status="private",
    )

"""
Grabs a trending post title from Reddit's public JSON endpoint.
No API key needed for read-only access to public subreddit listings.
"""
import os
import random
import requests

def fetch_trending_topic(subreddit: str = None) -> str:
    subreddit = subreddit or os.getenv("TOPIC_SUBREDDIT", "news")
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=15"
    headers = {"User-Agent": "ai-shorts-bot/1.0"}

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    posts = resp.json()["data"]["children"]

    # filter out stickied/pinned posts, pick a random one from the rest
    candidates = [p["data"]["title"] for p in posts if not p["data"].get("stickied")]
    if not candidates:
        raise RuntimeError("No candidate topics found — try a different subreddit")

    return random.choice(candidates)


if __name__ == "__main__":
    print(fetch_trending_topic())

"""
Returns the topic for today's short — either passed in manually
via GitHub Actions' workflow_dispatch input, or a fallback default.
"""
import os

def fetch_trending_topic(subreddit: str = None) -> str:
    topic = os.getenv("MANUAL_TOPIC", "").strip()
    if topic:
        return topic
    return "a surprising everyday life hack"  # fallback if left blank

if __name__ == "__main__":
    print(fetch_trending_topic())

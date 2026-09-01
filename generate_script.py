"""
Turns a topic into a punchy 30-60 second commentary script.
Uses Anthropic's API if ANTHROPIC_API_KEY is set, otherwise falls back to OpenAI.
"""
import os

PROMPT_TEMPLATE = """You write short, punchy YouTube Shorts commentary scripts.

Topic: "{topic}"

Write a 30-45 second spoken script (about 90-110 words) reacting to this topic.
Rules:
- Sarcastic, opinionated, energetic tone
- Hook in the first line — no throat-clearing intros
- Short sentences, easy for a text-to-speech voice to read naturally
- End on a punchy one-liner, not a fade-out
- Output ONLY the spoken script, no stage directions, no titles, no quotation marks
"""

def generate_script(topic: str) -> str:
    prompt = PROMPT_TEMPLATE.format(topic=topic)

    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()

    elif os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()

    else:
        raise RuntimeError(
            "No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file."
        )


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    from fetch_topic import fetch_trending_topic

    topic = fetch_trending_topic()
    print(f"Topic: {topic}\n")
    print(generate_script(topic))

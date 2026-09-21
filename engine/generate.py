import os, json, urllib.request
from pathlib import Path

def load_config(project):
    return json.loads(
        (Path("projects") / project / "project.json").read_text(encoding="utf-8")
    )

def ask_gemini(config):
    key = os.environ["GEMINI_API_KEY"]

    prompt = f"""
You are the content brain of an automated short-video engine.

Project: {config['project_name']}
Topic: {config['content_source']['topic']}
Description: {config['content_source']['description']}
Language: {config['language']}
Duration: {config['video']['duration_seconds']} seconds.

Create ONE short-form vertical video concept.

Return ONLY valid JSON:
{{
  "hook": "short attention-grabbing hook",
  "body": "very short voiceover/body text",
  "cta": "short call to action",
  "caption": "social media caption",
  "hashtags": ["tag1","tag2","tag3","tag4"]
}}
"""

    model = "gemini-1.5-flash"

    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }).encode()

    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())

    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text), model

def main():
    import sys
    project = sys.argv[1] if len(sys.argv) > 1 else "demo"

    config = load_config(project)
    content, model = ask_gemini(config)

    out = Path("output") / project
    out.mkdir(parents=True, exist_ok=True)

    (out / "content.json").write_text(
        json.dumps(content, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("AI content generated successfully.")
    print("Model:", model)
    print(json.dumps(content, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

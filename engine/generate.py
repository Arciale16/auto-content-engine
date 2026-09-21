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

    # Ask the API which current models this key can actually use.
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    )
    with urllib.request.urlopen(req) as r:
        models = json.loads(r.read())

    candidates = []
    for m in models.get("models", []):
        methods = m.get("supportedGenerationMethods", [])
        name = m.get("name", "").replace("models/", "")
        if "generateContent" in methods and "flash" in name.lower():
            candidates.append(name)

    if not candidates:
        raise RuntimeError("No compatible Gemini Flash model available.")

    # Prefer newer Flash models automatically.
    candidates.sort(reverse=True)
    model = candidates[0]

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

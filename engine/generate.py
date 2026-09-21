import os
import json
import urllib.request
from pathlib import Path


def load_config(project):
    path = Path("projects") / project / "project.json"
    return json.loads(path.read_text(encoding="utf-8"))


def ask_gemini(config):
    key = os.environ["GEMINI_API_KEY"]

    # Trova automaticamente un modello disponibile
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    )

    with urllib.request.urlopen(req) as r:
        models = json.loads(r.read())

    available = []

    for model in models.get("models", []):
        name = model.get("name", "").replace("models/", "")
        methods = model.get("supportedGenerationMethods", [])

        if "generateContent" in methods:
            available.append(name)

    if not available:
        raise RuntimeError("No Gemini models available")

    mpreferred = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

model_name = None

for p in preferred:
    if p in available:
        model_name = p
        break

if model_name is None:
    model_name = available[0]

print("Using model:", model_name)

    print("Using model:", model_name)

    prompt = f"""
Create a short vertical video concept.

Project:
{config['project_name']}

Topic:
{config['content_source']['topic']}

Description:
{config['content_source']['description']}

Language:
{config['language']}

Duration:
{config['video']['duration_seconds']} seconds

Return ONLY JSON:

{{
"hook":"",
"body":"",
"cta":"",
"caption":"",
"hashtags":[]
}}
"""

    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}",
        data=payload,
        headers={
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    return json.loads(text), model_name


def main():
    import sys

    project = sys.argv[1] if len(sys.argv) > 1 else "demo"

    config = load_config(project)

    content, model = ask_gemini(config)

    output = Path("output") / project
    output.mkdir(parents=True, exist_ok=True)

    (output / "content.json").write_text(
        json.dumps(content, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("SUCCESS")
    print("MODEL:", model)
    print(json.dumps(content, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
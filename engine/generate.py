import os
import json
import sys
from pathlib import Path
from google import genai


def load_config(project):
    path = Path("projects") / project / "project.json"
    return json.loads(path.read_text(encoding="utf-8"))


def generate_content(config):
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

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

Return only JSON:

{{
"hook":"",
"body":"",
"cta":"",
"caption":"",
"hashtags":[]
}}
"""

    models_to_try = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

last_error = None

for model in models_to_try:
    try:
        print("Trying model:", model)

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        return json.loads(response.text)

    except Exception as e:
        print("Failed:", model)
        last_error = e

raise last_error

    return json.loads(response.text)


def main():
    project = sys.argv[1] if len(sys.argv) > 1 else "demo"

    config = load_config(project)

    result = generate_content(config)

    output = Path("output") / project
    output.mkdir(parents=True, exist_ok=True)

    (output / "content.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("SUCCESS")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
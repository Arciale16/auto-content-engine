import os
import json
import sys
import time
from pathlib import Path
from google import genai


def load_config(project):
    config_file = Path("projects") / project / "project.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Missing project file: {config_file}"
        )

    return json.loads(
        config_file.read_text(encoding="utf-8")
    )


def get_models(client):
    print("Checking available Gemini models...")

    models = client.models.list()

    available = []

    for model in models:
        name = model.name.replace("models/", "")

        if "gemini" in name.lower():
            available.append(name)

    print("")
    print("Available models:")

    for model in available:
        print("-", model)

    return available


def select_model(models):

    # Ordine di preferenza
    preferred = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3-flash",
        "gemini-flash-latest"
    ]

    for item in preferred:
        if item in models:
            return item

    # fallback: qualsiasi flash recente
    for model in models:
        if "flash" in model.lower():
            return model

    raise RuntimeError(
        "No compatible Gemini Flash model found"
    )


def create_prompt(config):

    return f"""
You are an automatic content creation engine.

Create one short vertical video idea.

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

Return ONLY valid JSON.

Format:

{{
"hook": "",
"body": "",
"cta": "",
"caption": "",
"hashtags": []
}}
"""


def generate_with_gemini(config):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    available_models = get_models(client)

    model = select_model(available_models)

    print("")
    print("Selected model:")
    print(model)
    print("")

    prompt = create_prompt(config)

    last_error = None

    for attempt in range(1, 4):

        try:

            print(
                f"Generation attempt {attempt}/3"
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            text = response.text.strip()

            return json.loads(text)


        except Exception as error:

            print("")
            print("Generation error:")
            print(error)
            print("")

            last_error = error

            if attempt < 3:
                print(
                    "Waiting 20 seconds before retry..."
                )

                time.sleep(20)


    raise last_error


def save_output(project, content):

    output_folder = Path("output") / project

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_folder / "content.json"

    output_file.write_text(
        json.dumps(
            content,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("")
    print("======================")
    print("CONTENT GENERATED")
    print("======================")
    print(output_file)


def main():

    project = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "demo"
    )

    print("")
    print("======================")
    print("AUTO CONTENT ENGINE")
    print("======================")
    print("Project:", project)
    print("")

    config = load_config(project)

    content = generate_with_gemini(config)

    save_output(
        project,
        content
    )

    print("")
    print(json.dumps(
        content,
        indent=2,
        ensure_ascii=False
    ))


if __name__ == "__main__":
    main()
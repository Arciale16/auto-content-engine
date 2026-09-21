import os
import json
import sys
import time
from pathlib import Path
from google import genai


def load_config(project):
    path = Path("projects") / project / "project.json"

    if not path.exists():
        raise FileNotFoundError(f"Project not found: {project}")

    return json.loads(path.read_text(encoding="utf-8"))


def find_available_models(client):
    print("Checking available Gemini models...")

    models = client.models.list()

    available = []

    for model in models:
        name = model.name.replace("models/", "")

        methods = getattr(
            model,
            "supported_actions",
            []
        )

        # fallback: accettiamo i modelli Gemini generativi
        if "gemini" in name.lower():
            available.append(name)

    if not available:
        raise RuntimeError(
            "No Gemini models available for this API key"
        )

    print("Available models:")
    for m in available:
        print("-", m)

    return available


def choose_model(models):

    preferred_words = [
        "flash",
        "pro"
    ]

    # preferiamo modelli veloci/economici
    for word in preferred_words:
        for model in models:
            if word in model.lower():
                return model

    return models[0]


def generate_content(config):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    models = find_available_models(client)

    model = choose_model(models)

    print("")
    print("Selected model:")
    print(model)
    print("")

    prompt = f"""
You are the AI content engine.

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

Return ONLY valid JSON:

{{
"hook":"",
"body":"",
"cta":"",
"caption":"",
"hashtags":[]
}}
"""


    last_error = None

    for attempt in range(3):

        try:

            print(
                f"Generation attempt {attempt + 1}/3"
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return json.loads(response.text)


        except Exception as error:

            print("Generation failed:")
            print(error)

            last_error = error

            time.sleep(20)


    raise last_error


def main():

    project = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "demo"
    )

    config = load_config(project)

    result = generate_content(config)


    output = Path("output") / project

    output.mkdir(
        parents=True,
        exist_ok=True
    )


    file = output / "content.json"

    file.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print("")
    print("======================")
    print("CONTENT GENERATED")
    print("======================")
    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
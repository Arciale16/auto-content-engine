import json
import sys
from pathlib import Path

from engine.providers import gemini
from engine.providers import fallback


def load_config(project):
    config_file = Path("projects") / project / "project.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Project not found: {config_file}"
        )

    return json.loads(
        config_file.read_text(
            encoding="utf-8"
        )
    )


def create_prompt(config):

    return f"""
You are an automatic short video content engine.

Create a vertical social media video script.

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

Return ONLY JSON.

Format:

{{
"hook": "",
"body": "",
"cta": "",
"caption": "",
"hashtags": []
}}
"""


def generate_content(config):

    prompt = create_prompt(config)

    print("")
    print("======================")
    print("CONTENT GENERATION")
    print("======================")

    try:
        print("Using Gemini AI...")
        content = gemini.generate(prompt)

        print("Gemini success")

        return content

    except Exception as error:

        print("")
        print("Gemini failed:")
        print(error)
        print("")

        print("Using fallback engine...")

        content = fallback.generate(prompt)

        print("Fallback success")

        return content


def save_content(project, content):

    output_folder = (
        Path("output")
        / project
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_folder
        / "content.json"
    )

    output_file.write_text(
        json.dumps(
            content,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return output_file


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

    print(
        "Project:",
        project
    )

    config = load_config(project)

    content = generate_content(
        config
    )

    file = save_content(
        project,
        content
    )

    print("")
    print("======================")
    print("CONTENT READY")
    print("======================")

    print(
        "Saved:",
        file
    )

    print("")

    print(
        json.dumps(
            content,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
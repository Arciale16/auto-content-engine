import json
from pathlib import Path

def load_project(project="demo"):
    path = Path("projects") / project / "project.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = load_project()
    print("\nAUTO CONTENT ENGINE")
    print("-------------------")
    print(f"Project: {config['project_name']}")
    print(f"Topic: {config['content_source']['topic']}")
    print(f"Language: {config['language']}")
    print(f"Video: {config['video']['width']}x{config['video']['height']}")
    print(f"Duration: {config['video']['duration_seconds']} seconds")
    print("\nEngine configuration loaded successfully.")

if __name__ == "__main__":
    main()

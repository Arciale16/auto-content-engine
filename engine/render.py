import json
import subprocess
import sys
from pathlib import Path


project = sys.argv[1] if len(sys.argv) > 1 else "demo"


config_path = Path("projects") / project / "project.json"
content_path = Path("output") / project / "content.json"


config = json.loads(
    config_path.read_text(encoding="utf-8")
)

content = json.loads(
    content_path.read_text(encoding="utf-8")
)


output = Path("output") / project
output.mkdir(parents=True, exist_ok=True)


hook = content.get("hook", "AI generated this idea")
body = content.get("body", "")
cta = content.get("cta", "Follow for more")


hook_file = output / "hook.txt"
body_file = output / "body.txt"
cta_file = output / "cta.txt"


hook_file.write_text(hook, encoding="utf-8")
body_file.write_text(body, encoding="utf-8")
cta_file.write_text(cta, encoding="utf-8")


video = output / "video.mp4"


cmd = [
    "ffmpeg",
    "-y",

    "-f",
    "lavfi",
    "-i",
    "color=c=black:s=1080x1920:d=10",

    "-vf",
    (
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "textfile='"
        + str(hook_file)
        +
        "':"
        "fontcolor=white:"
        "fontsize=80:"
        "x=(w-text_w)/2:"
        "y=500:"
        "enable='between(t,0,3)',"

        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        "textfile='"
        + str(body_file)
        +
        "':"
        "fontcolor=white:"
        "fontsize=45:"
        "x=(w-text_w)/2:"
        "y=850:"
        "enable='between(t,3,8)',"

        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "textfile='"
        + str(cta_file)
        +
        "':"
        "fontcolor=yellow:"
        "fontsize=60:"
        "x=(w-text_w)/2:"
        "y=1400:"
        "enable='between(t,8,10)'"
    ),

    "-c:v",
    "libx264",

    "-pix_fmt",
    "yuv420p",

    str(video)
]


subprocess.run(
    cmd,
    check=True
)


print("VIDEO CREATED:")
print(video)
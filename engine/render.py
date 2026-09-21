import json
import subprocess
import sys
from pathlib import Path


project = sys.argv[1] if len(sys.argv) > 1 else "demo"


content_file = Path("output") / project / "content.json"

if not content_file.exists():
    raise FileNotFoundError("Missing content.json")


content = json.loads(
    content_file.read_text(encoding="utf-8")
)


background = Path(
    "assets/processed/processed.png"
)

if not background.exists():
    raise FileNotFoundError(
        "Missing processed image"
    )


output = Path("output") / project
output.mkdir(
    parents=True,
    exist_ok=True
)


video = output / "video.mp4"


hook = content.get(
    "hook",
    "AI is changing everything"
)

body = content.get(
    "body",
    ""
)

cta = content.get(
    "cta",
    "Follow for more"
)


hook_file = output / "hook.txt"
body_file = output / "body.txt"
cta_file = output / "cta.txt"


hook_file.write_text(
    hook,
    encoding="utf-8"
)

body_file.write_text(
    body,
    encoding="utf-8"
)

cta_file.write_text(
    cta,
    encoding="utf-8"
)


# Font Windows
font = "C\\:/Windows/Fonts/arial.ttf"
font_bold = "C\\:/Windows/Fonts/arialbd.ttf"


command = [

    "ffmpeg",
    "-y",

    "-loop",
    "1",

    "-i",
    str(background),


    "-filter_complex",

    (
        "[0:v]"
        "scale=1080:1920,"
        "zoompan="
        "z='min(zoom+0.001,1.12)':"
        "d=250:"
        "s=1080x1920,"

        "drawbox="
        "x=0:y=0:"
        "w=1080:h=1920:"
        "color=black@0.35:"
        "t=fill,"

        "drawtext="
        f"fontfile='{font_bold}':"
        f"textfile='{hook_file}':"
        "fontcolor=white:"
        "fontsize=75:"
        "x=(w-text_w)/2:"
        "y=400:"
        "box=1:"
        "boxcolor=black@0.4:"
        "boxborderw=20:"
        "enable='between(t,0,3)',"


        "drawtext="
        f"fontfile='{font}':"
        f"textfile='{body_file}':"
        "fontcolor=white:"
        "fontsize=45:"
        "x=(w-text_w)/2:"
        "y=850:"
        "box=1:"
        "boxcolor=black@0.35:"
        "boxborderw=15:"
        "enable='between(t,3,8)',"


        "drawtext="
        f"fontfile='{font_bold}':"
        f"textfile='{cta_file}':"
        "fontcolor=yellow:"
        "fontsize=65:"
        "x=(w-text_w)/2:"
        "y=1450:"
        "box=1:"
        "boxcolor=black@0.4:"
        "boxborderw=20:"
        "enable='between(t,8,10)'"
    ),


    "-t",
    "10",

    "-c:v",
    "libx264",

    "-pix_fmt",
    "yuv420p",

    str(video)
]


subprocess.run(
    command,
    check=True
)


print("====================")
print("VIDEO CREATED")
print(video)
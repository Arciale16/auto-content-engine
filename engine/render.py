import json
import subprocess
import sys
from pathlib import Path


project = sys.argv[1] if len(sys.argv) > 1 else "demo"


# Legge contenuto generato dall'AI
content_file = Path("output") / project / "content.json"

if not content_file.exists():
    raise FileNotFoundError(
        "Content file not found"
    )


content = json.loads(
    content_file.read_text(
        encoding="utf-8"
    )
)


# Cerca automaticamente una immagine
background_folder = Path("assets/backgrounds")

images = []

for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
    images.extend(
        background_folder.glob(ext)
    )


if not images:
    raise FileNotFoundError(
        "No image found in assets/backgrounds"
    )


background = images[0]

print("Using background:")
print(background)


# Output
output = Path("output") / project

output.mkdir(
    parents=True,
    exist_ok=True
)


video = output / "video.mp4"


# Testi
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


# FFmpeg
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
        "z='min(zoom+0.0015,1.15)':"
        "d=250:"
        "s=1080x1920,"
        
        # Hook
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"textfile='{hook_file}':"
        "fontcolor=white:"
        "fontsize=80:"
        "x=(w-text_w)/2:"
        "y=450:"
        "enable='between(t,0,3)',"

        # Body
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        f"textfile='{body_file}':"
        "fontcolor=white:"
        "fontsize=45:"
        "x=(w-text_w)/2:"
        "y=850:"
        "enable='between(t,3,8)',"

        # CTA
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"textfile='{cta_file}':"
        "fontcolor=yellow:"
        "fontsize=65:"
        "x=(w-text_w)/2:"
        "y=1450:"
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


print("")
print("====================")
print("VIDEO CREATED")
print("====================")
print(video)
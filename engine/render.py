import json, subprocess, sys
from pathlib import Path

project = sys.argv[1] if len(sys.argv) > 1 else "demo"

config = json.loads(
    (Path("projects") / project / "project.json").read_text(encoding="utf-8")
)

content = json.loads(
    (Path("output") / project / "content.json").read_text(encoding="utf-8")
)

out = Path("output") / project
out.mkdir(parents=True, exist_ok=True)

text = content["hook"] + "\n\n" + content["body"] + "\n\n" + content["cta"]

textfile = out / "video_text.txt"
textfile.write_text(text, encoding="utf-8")

video = out / "video.mp4"

duration = config["video"]["duration_seconds"]

# Simple first renderer. Later templates replace this without changing the engine.
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi",
    "-i", f"color=c=0x111111:s=1080x1920:d={duration}",
    "-vf",
    "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
    f"textfile='{textfile}':fontcolor=white:fontsize=58:"
    "x=(w-text_w)/2:y=(h-text_h)/2:"
    "line_spacing=20",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    str(video)
]

subprocess.run(cmd, check=True)

print("VIDEO CREATED:", video)

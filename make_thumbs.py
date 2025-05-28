"""
Save as make_thumbs.py and run inside your project root:

python make_thumbs.py

It walks static/videos/*.mp4 and writes static/thumbnails/<same>.jpg
Requires ffmpeg installed in PATH.
"""
import subprocess, pathlib, sys

videos_dir = pathlib.Path("static/videos")
thumbs_dir = pathlib.Path("static/thumbnails")
thumbs_dir.mkdir(parents=True, exist_ok=True)

for mp4 in videos_dir.glob("*.mp4"):
    jpg = thumbs_dir / (mp4.stem + ".jpg")
    if jpg.exists():
        continue
    # Extract the very first frame (at 0.1 s for reliability)
    cmd = [
        "ffmpeg", "-loglevel", "error",
        "-i", str(mp4),
        "-ss", "0.1",  # seek
        "-vframes", "1",
        "-q:v", "2",   # quality 2 (~95%)
        str(jpg)
    ]
    print("→", jpg.name)
    if subprocess.call(cmd):
        print("  ffmpeg failed!", file=sys.stderr)

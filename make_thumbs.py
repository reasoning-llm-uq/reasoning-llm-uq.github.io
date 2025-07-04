# %%
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

for mp4 in videos_dir.glob("**/*.mp4"):
    jpg = thumbs_dir / (mp4.stem + ".jpg")
    if jpg.exists():
        continue
    # Extract the last frame
    # First, get the video duration using ffprobe
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(mp4)
        ],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    # Seek to just before the end (duration - 0.1s)
    seek_time = max(0, duration - 0.1)
    cmd = [
        "ffmpeg", "-loglevel", "error",
        "-ss", str(seek_time),
        "-i", str(mp4),
        "-vframes", "1",
        "-q:v", "2",
        str(jpg)
    ]
    print("→", jpg.name)
    if subprocess.call(cmd):
        print("  ffmpeg failed!", file=sys.stderr)

# %%

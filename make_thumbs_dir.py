import subprocess, pathlib, sys

videos_dir = pathlib.Path("static/videos")
thumbs_dir = pathlib.Path("static/thumbnails")

for mp4 in videos_dir.glob("**/*.mp4"):
    # Compute relative path from videos_dir and use that in thumbs_dir
    rel_path = mp4.relative_to(videos_dir).with_suffix(".jpg")
    jpg_path = thumbs_dir / rel_path
    jpg_path.parent.mkdir(parents=True, exist_ok=True)

    if jpg_path.exists():
        continue

    # Extract the very first frame (at 0.1 s for reliability)
    cmd = [
        "ffmpeg", "-loglevel", "error",
        "-i", str(mp4),
        "-ss", "0.1",  # seek
        "-vframes", "1",
        "-q:v", "2",   # quality 2 (~95%)
        str(jpg_path)
    ]
    print("→", jpg_path)
    if subprocess.call(cmd):
        print("  ffmpeg failed!", file=sys.stderr)

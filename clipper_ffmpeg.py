
import csv
import subprocess
from pathlib import Path

import imageio_ffmpeg
from moviepy import VideoFileClip

# Project files
FOLDER = Path(__file__).resolve().parent
VIDEO = FOLDER / "gameplay.mp4"

CSV = FOLDER / "combined_highlights.csv"

OUTPUT = FOLDER / "clips_with_audio"

OUTPUT.mkdir(exist_ok=True)

# Find FFmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# Read highlight timestamps
with open(CSV, newline="") as file:
    reader = csv.DictReader(file)
    timestamps = [
        float(row["timestamp_seconds"])
        for row in reader
    ]

# Get video duration
with VideoFileClip(str(VIDEO)) as video:
    duration = video.duration

print("Exporting highlights with audio!")

for number, timestamp in enumerate(timestamps, 1):

    start = max(0, timestamp - 10)
    end = min(duration, timestamp + 10)

    if end <= start:
        continue

    output_file = OUTPUT / f"clip_{number}.mp4"

    command = [
        ffmpeg,
        "-y",
        "-ss", str(start),
        "-i", str(VIDEO),
        "-t", str(end - start),
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_file)
    ]

    print(f"Exporting clip {number}...")

    subprocess.run(command, check=True)

print("All clips exported successfully!")
print(f"Saved to: {OUTPUT}")

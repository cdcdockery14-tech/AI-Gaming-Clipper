
import csv
from pathlib import Path
from moviepy import VideoFileClip

# PROJECT SETTINGS
PROJECT_FOLDER = Path(__file__).resolve().parent

VIDEO_PATH = PROJECT_FOLDER / "gameplay.mp4"
CSV_PATH = PROJECT_FOLDER / "highlights.csv"
OUTPUT_FOLDER = PROJECT_FOLDER / "clips"

# Clip settings
SECONDS_BEFORE = 10
SECONDS_AFTER = 10

print("AI Gaming Clipper - Video Exporter")
print("----------------------------------")

# Check required files
if not VIDEO_PATH.exists():
    print("ERROR: gameplay.mp4 not found!")
    raise SystemExit(1)

if not CSV_PATH.exists():
    print("ERROR: highlights.csv not found!")
    raise SystemExit(1)

# Create output folder automatically
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Read detected highlight timestamps
highlights = []

with open(CSV_PATH, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        timestamp = float(row["timestamp_seconds"])
        highlights.append(timestamp)

if not highlights:
    print("No highlights were found.")
    raise SystemExit(1)

print(f"Found {len(highlights)} highlights.")

# Open the original gameplay video
with VideoFileClip(str(VIDEO_PATH)) as video:

    duration = video.duration

    for number, timestamp in enumerate(highlights, 1):

        # Start 10 seconds before the highlight
        start_time = max(0, timestamp - SECONDS_BEFORE)

        # End 10 seconds after the highlight
        end_time = min(duration, timestamp + SECONDS_AFTER)

        if end_time <= start_time:
            print(f"Skipping invalid highlight {number}")
            continue

        output_path = OUTPUT_FOLDER / f"clip_{number}.mp4"

        print(f"\nExporting highlight {number}...")
        print(f"Start: {start_time:.1f} seconds")
        print(f"End: {end_time:.1f} seconds")

        # Cut the video
        
        # Cut the video
        clip = video.subclipped(start_time, end_time)

        # Export as MP4
        clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio=False,
            preset="ultrafast",
            logger="bar"
        )

        clip.close()

print(f"Find your clips inside: {OUTPUT_FOLDER}")

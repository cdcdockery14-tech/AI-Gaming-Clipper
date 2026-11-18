
import csv
import json
from pathlib import Path

import cv2

FOLDER = Path(__file__).resolve().parent
VIDEO = FOLDER / "gameplay.mp4"
HIGHLIGHTS = FOLDER / "combined_highlights.csv"
CLIPS = FOLDER / "clips_with_audio"
OUTPUT = FOLDER / "report.json"

# Read video metadata
capture = cv2.VideoCapture(str(VIDEO))

if not capture.isOpened():
    raise SystemExit("Could not open gameplay.mp4")

fps = capture.get(cv2.CAP_PROP_FPS)
frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

capture.release()

if fps <= 0:
    raise SystemExit("Invalid video FPS")

duration = frame_count / fps

# Read selected highlights
with open(HIGHLIGHTS, newline="") as file:
    reader = csv.DictReader(file)
    highlights = list(reader)

# Count exported clips
exported_clips = sorted(CLIPS.glob("clip_*.mp4"))

scores = [
    float(item["combined_score"])
    for item in highlights
]

average_score = (
    sum(scores) / len(scores)
    if scores else 0
)

report = {
    "project": "AI Automated Gaming Clipper",
    "video_duration_seconds": round(duration, 2),
    "video_resolution": f"{width}x{height}",
    "video_fps": round(fps, 2),
    "highlights_detected": len(highlights),
    "clips_exported": len(exported_clips),
    "average_activity_score": round(average_score, 2),
    "highlights": [
        {
            "timestamp_seconds": float(
                item["timestamp_seconds"]
            ),
            "combined_score": round(
                float(item["combined_score"]), 2
            )
        }
        for item in highlights
    ]
}

with open(OUTPUT, "w") as file:
    json.dump(report, file, indent=4)

print("\nAI GAMING CLIPPER REPORT")
print("-----------------------------")
print(f"Video duration: {duration:.1f} seconds")
print(f"Resolution: {width}x{height}")
print(f"FPS: {fps:.1f}")
print(f"Highlights detected: {len(highlights)}")
print(f"Clips exported: {len(exported_clips)}")
print(f"Average activity score: {average_score:.1f}")
print("\nReport saved to report.json")

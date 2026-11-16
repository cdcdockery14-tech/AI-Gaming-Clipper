
import cv2
import numpy as np
import csv
from pathlib import Path

# SETTINGS
VIDEO_PATH = Path(__file__).resolve().parent / "gameplay.mp4"
SAMPLE_SECONDS = 0.5
HIGHLIGHT_COUNT = 5
MIN_GAP_SECONDS = 10

print("AI Gaming Clipper - Highlight Detector")
print("--------------------------------------")

# Open the gameplay recording
video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    print("ERROR: Could not open gameplay.mp4")
    raise SystemExit(1)

fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

if fps <= 0:
    print("ERROR: Invalid video FPS")
    video.release()
    raise SystemExit(1)

duration = total_frames / fps
step = max(1, int(fps * SAMPLE_SECONDS))

print(f"Video duration: {duration:.1f} seconds")
print("Scanning gameplay...")

previous_frame = None
activity_scores = []

# Scan sampled frames
for frame_number in range(0, total_frames, step):

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = video.read()

    if not success:
        continue

    # Resize for faster analysis
    frame = cv2.resize(frame, (320, 180))

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Reduce visual noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    if previous_frame is not None:

        # Measure differences between frames
        difference = cv2.absdiff(previous_frame, gray)

        score = float(np.mean(difference))
        timestamp = frame_number / fps

        activity_scores.append((timestamp, score))

    previous_frame = gray

video.release()

if not activity_scores:
    print("Not enough frames to analyze.")
    raise SystemExit(1)

# Rank moments by visual activity
ranked = sorted(
    activity_scores,
    key=lambda item: item[1],
    reverse=True
)

highlights = []

for timestamp, score in ranked:

    # Avoid choosing moments too close together
    too_close = any(
        abs(timestamp - existing[0]) < MIN_GAP_SECONDS
        for existing in highlights
    )

    if not too_close:
        highlights.append((timestamp, score))

    if len(highlights) >= HIGHLIGHT_COUNT:
        break

# Put highlights in chronological order
highlights.sort()

print("\nPOTENTIAL GAMEPLAY HIGHLIGHTS")
print("-----------------------------")

for number, (timestamp, score) in enumerate(highlights, 1):

    minutes = int(timestamp // 60)
    seconds = int(timestamp % 60)

    print(
        f"Highlight {number}: "
        f"{minutes:02d}:{seconds:02d} "
        f"| Activity score: {score:.2f}"
    )

# Save results to CSV
output_path = VIDEO_PATH.parent / "highlights.csv"

with open(output_path, "w", newline="") as file:

    writer = csv.writer(file)
    writer.writerow(["timestamp_seconds", "activity_score"])
    writer.writerows(highlights)

print("\nSaved results to highlights.csv")
print("Highlight detection complete!")
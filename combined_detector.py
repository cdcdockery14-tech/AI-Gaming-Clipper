
import csv
from pathlib import Path

import cv2
import numpy as np

# Project settings
FOLDER = Path(__file__).resolve().parent
VIDEO = FOLDER / "gameplay.mp4"
AUDIO_CSV = FOLDER / "audio_scores.csv"
OUTPUT = FOLDER / "combined_highlights.csv"

SAMPLE_SECONDS = 0.5
VISUAL_WEIGHT = 0.6
AUDIO_WEIGHT = 0.4
HIGHLIGHT_COUNT = 5
MIN_GAP_SECONDS = 20

print("AI Gaming Clipper - Combined Detector")
print("------------------------------------")

# STEP 1: Load audio activity scores
audio_data = np.genfromtxt(
    AUDIO_CSV,
    delimiter=",",
    names=True
)

audio_data = np.atleast_1d(audio_data)

audio_times = audio_data["timestamp_seconds"]
audio_scores = audio_data["audio_score"]

if len(audio_scores) == 0:
    print("ERROR: No audio scores found.")
    raise SystemExit(1)

# STEP 2: Analyze visual activity again
video = cv2.VideoCapture(str(VIDEO))

if not video.isOpened():
    print("ERROR: Could not open gameplay.mp4")
    raise SystemExit(1)

fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

if fps <= 0:
    print("ERROR: Invalid video FPS")
    video.release()
    raise SystemExit(1)

step = max(1, int(fps * SAMPLE_SECONDS))

visual_times = []
visual_scores = []
previous_frame = None

print("Scanning visual activity...")

for frame_number in range(0, total_frames, step):

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = video.read()

    if not success:
        continue

    frame = cv2.resize(frame, (320, 180))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    if previous_frame is not None:
        difference = cv2.absdiff(previous_frame, gray)
        score = float(np.mean(difference))

        visual_times.append(frame_number / fps)
        visual_scores.append(score)

    previous_frame = gray

video.release()

if not visual_scores:
    print("ERROR: Not enough video frames.")
    raise SystemExit(1)

visual_times = np.array(visual_times)
visual_scores = np.array(visual_scores)

# STEP 3: Normalize scores to 0-100
def normalize(values):
    values = np.asarray(values, dtype=float)

    low = np.percentile(values, 5)
    high = np.percentile(values, 95)

    if high <= low:
        return np.zeros_like(values)

    normalized = (values - low) / (high - low)
    return np.clip(normalized * 100, 0, 100)

visual_normalized = normalize(visual_scores)
audio_normalized = normalize(audio_scores)

# STEP 4: Align audio with video timestamps
aligned_audio = np.interp(
    visual_times,
    audio_times,
    audio_normalized,
    left=audio_normalized[0],
    right=audio_normalized[-1]
)

# STEP 5: Calculate combined scores
combined_scores = (
    VISUAL_WEIGHT * visual_normalized
    + AUDIO_WEIGHT * aligned_audio
)

# STEP 6: Rank potential highlights
ranked_indices = np.argsort(combined_scores)[::-1]

highlights = []

for index in ranked_indices:
    timestamp = float(visual_times[index])
    score = float(combined_scores[index])

    too_close = any(
        abs(timestamp - existing[0]) < MIN_GAP_SECONDS
        for existing in highlights
    )

    if not too_close:
        highlights.append((timestamp, score))

    if len(highlights) >= HIGHLIGHT_COUNT:
        break

highlights.sort()

# STEP 7: Save timestamps for the exporter
with open(OUTPUT, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "timestamp_seconds",
        "combined_score"
    ])
    writer.writerows(highlights)

print("\nTOP COMBINED HIGHLIGHTS")
print("-----------------------")

for number, (timestamp, score) in enumerate(highlights, 1):
    minutes = int(timestamp // 60)
    seconds = int(timestamp % 60)

    print(
        f"Highlight {number}: "
        f"{minutes:02d}:{seconds:02d} "
        f"| Combined score: {score:.1f}"
    )

print("\nSaved to combined_highlights.csv")
print("Combined detection complete!")


import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

# Project settings
FOLDER = Path(__file__).resolve().parent
VIDEO = FOLDER / "gameplay.mp4"
OUTPUT = FOLDER / "audio_scores.csv"

SAMPLE_RATE = 8000
WINDOW_SECONDS = 0.5

print("AI Gaming Clipper - Audio Analyzer")

if not VIDEO.exists():
    print("ERROR: gameplay.mp4 not found!")
    raise SystemExit(1)

# Get video duration
capture = cv2.VideoCapture(str(VIDEO))
fps = capture.get(cv2.CAP_PROP_FPS)
frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
capture.release()

if fps <= 0:
    print("ERROR: Invalid video FPS")
    raise SystemExit(1)

duration = frames / fps

# Find FFmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# Extract audio as raw samples
command = [
    ffmpeg,
    "-v", "error",
    "-i", str(VIDEO),
    "-map", "0:a:0",
    "-vn",
    "-ac", "1",
    "-ar", str(SAMPLE_RATE),
    "-f", "f32le",
    "-"
]

print("Analyzing gameplay audio...")

result = subprocess.run(
    command,
    capture_output=True
)

if result.returncode != 0:
    print("ERROR: Could not extract audio.")
    print(result.stderr.decode(errors="replace"))
    raise SystemExit(1)

audio = np.frombuffer(
    result.stdout,
    dtype=np.float32
)

if len(audio) == 0:
    print("ERROR: No audio samples found.")
    raise SystemExit(1)

window_size = int(SAMPLE_RATE * WINDOW_SECONDS)

scores = []

for start in range(0, len(audio), window_size):

    chunk = audio[start:start + window_size]

    if len(chunk) == 0:
        continue

    # RMS measures audio signal intensity
    rms = float(np.sqrt(
        np.mean(np.square(chunk.astype(np.float64)))
    ))

    timestamp = start / SAMPLE_RATE
    scores.append((timestamp, rms))

# Save results
np.savetxt(
    OUTPUT,
    np.array(scores),
    delimiter=",",
    header="timestamp_seconds,audio_score",
    comments="",
    fmt="%.6f"
)

print(f"Analyzed {len(scores)} audio windows.")
print(f"Saved results to {OUTPUT.name}")
print("Audio analysis complete!")

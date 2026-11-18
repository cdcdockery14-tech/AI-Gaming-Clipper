
import subprocess
import sys
import time
from pathlib import Path

# Find the project folder
FOLDER = Path(__file__).resolve().parent

# Use the same Python environment
PYTHON = sys.executable

# Programs to run in order

STEPS = [
    ("Audio Analysis", "audio_detector.py"),
    ("Combined Highlight Detection", "combined_detector.py"),
    ("Video Export", "clipper_ffmpeg.py"),
    ("Performance Report", "report.py"),
]


print("=" * 45)
print("       AI AUTOMATED GAMING CLIPPER")
print("=" * 45)

# Check for gameplay recording
video = FOLDER / "gameplay.mp4"

if not video.exists():
    print("\nERROR: gameplay.mp4 was not found!")
    print("Place your OBS recording in the project folder.")
    sys.exit(1)

start_time = time.time()

# Run every step automatically
for number, (name, filename) in enumerate(STEPS, 1):

    print(f"\nSTEP {number}/{len(STEPS)}: {name}")
    print("-" * 45)

    command = [
        PYTHON,
        str(FOLDER / filename)
    ]

    result = subprocess.run(
        command,
        cwd=FOLDER
    )

    # Stop if a step fails
    if result.returncode != 0:
        print(f"\nERROR: {name} failed!")
        print("Fix the error above and try again.")
        sys.exit(result.returncode)

    print(f"\n{name} completed!")

elapsed = time.time() - start_time

print("\n" + "=" * 45)
print("         ALL STEPS COMPLETE!")
print("=" * 45)

print(f"\nTotal processing time: {elapsed:.1f} seconds")
print(f"Your clips are saved in:")
print(FOLDER / "clips_with_audio")


import cv2
from pathlib import Path

print("AI Gaming Clipper is starting!")

# Find the gameplay video
video_path = Path("gameplay.mp4")

if not video_path.exists():
    print("ERROR: gameplay.mp4 was not found!")
    print("Put your recording in the project folder.")
    raise SystemExit(1)

# Open the video
video = cv2.VideoCapture(str(video_path))

if not video.isOpened():
    print("ERROR: Could not open the video.")
    raise SystemExit(1)

# Read video information
fps = video.get(cv2.CAP_PROP_FPS)
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    print("ERROR: Could not read video FPS.")
    video.release()
    raise SystemExit(1)

duration = frame_count / fps

print("\nGAMEPLAY VIDEO INFORMATION")
print("--------------------------")
print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")
print(f"Total frames: {frame_count}")
print(f"Duration: {duration:.2f} seconds")

# Read the first frame
success, frame = video.read()

if success:
    print("\nFirst gameplay frame loaded successfully!")
    print(f"Frame shape: {frame.shape}")
else:
    print("\nCould not read the first frame.")

video.release()

print("\nVideo analysis finished!")

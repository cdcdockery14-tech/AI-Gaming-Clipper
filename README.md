
# AI Automated Gaming Clipper

An automated gameplay highlight detection and video clipping
pipeline built with Python, OpenCV, NumPy, and FFmpeg.

## Overview

This project analyzes recorded gameplay using computer vision
and audio signal processing to identify potential highlight
moments and automatically export short video clips.

The pipeline combines visual activity and audio intensity
to rank candidate highlights.

## Features

- Automatically analyzes gameplay recordings
- Detects visual activity using OpenCV
- Measures audio intensity using RMS
- Combines video and audio scores
- Selects the top five candidate highlights
- Exports MP4 clips with gameplay audio
- Runs the entire pipeline with one command

## Technologies

- Python
- OpenCV
- NumPy
- FFmpeg
- MoviePy
- Git and GitHub

## How It Works

1. Load gameplay.mp4
2. Analyze audio intensity
3. Analyze visual frame differences
4. Normalize and combine activity scores
5. Rank candidate highlight timestamps
6. Export 20-second highlight clips

## Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL

Enter the project folder:

cd AI-GAMING-CLIPPER

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Usage

Place a recording named gameplay.mp4 in the project folder.

Run:

python run.py

Finished clips will be saved in:

clips_with_audio/

## Current Detection Method

The current system uses heuristic activity scoring,
not a trained machine-learning classifier.

Visual activity contributes 60% of the combined score.
Audio activity contributes 40%.

This approach identifies candidate moments that may
contain exciting gameplay, but it does not yet recognize
specific events such as eliminations or match victories.

## Planned Improvements

- Gameplay event recognition using machine learning
- Highlight accuracy evaluation
- Support for different games
- Configurable highlight duration and count
- Improved audio track handling
- Optional graphical interface

## Project Purpose

Built as a personal AI engineering portfolio project
to practice Python programming, computer vision,
audio signal processing, video processing,
and automated pipeline development.

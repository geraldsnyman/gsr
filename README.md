
# Simple Screen Recorder

A lightweight tool to capture screen activity as a sequence of high-quality JPEG images. Designed for creating coding tutorials, timelapses, and security monitoring where playback speed is determined in post-production.

## Features
- **Image Sequence Output**: Saves captures as .jpg files for easy import into video editors (e.g., DaVinci Resolve).
- **Adjustable Sensitivity**: Only captures frames when significant changes occur, saving disk space.
- **Configurable Frame Rate**: Set your desired capture frequency.
- **Modern UI**: Clean, dark-mode interface.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/geraldsnyman/ScreenRecorder.git
    cd ScreenRecorder
    ```

    *Optional: Initialize Git to track your changes:*
    ```bash
    git init
    git add .
    git commit -m "Initial setup"
    ```

2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install system dependencies** (Linux only):
    ```bash
    sudo apt-get install python3-tk python3-dev scrot -y
    # Or for Fedora: sudo dnf install python3-tkinter
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application**:
    ```bash
    python src/main.py
    ```

2.  **Controls**:
    - **FPS**: Adjust the slider to set capture frequency.
    - **Sensitivity**: Adjust the threshold for motion detection (Higher = less sensitive, captures only big changes).
    - **Tile Size**: Adjust the granularity of detection (100% = Full Screen, 1% = Small Tiles). Lower percentage allows detecting smaller changes (like cursors) even with high sensitivity threshold.
    - **Quality**: Adjust the JPEG compression quality (1-100, default 100).
    - **Output**: Browse and select the destination folder for recordings.
    - **Start Recording**: Begins capturing the screen.
    - **Stop Recording**: Stops capture and saves the sequence in a timestamped folder.

## License
Freeware. Feel free to use and modify.

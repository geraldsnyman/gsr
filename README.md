
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

## Installation

1.  Clone the repository.
2.  Run the automated setup script:
    ```bash
    ./setup.sh
    ```
    *This script will:*
    - *Install necessary system dependencies (like `python3-tk`).*
    - *Create a Python virtual environment.*
    - *Install all required Python libraries from `requirements.txt`.*

3.  (Optional) Install Desktop Entry (Linux):
    ```bash
    python3 setup_desktop.py
    ```

## Usage

1.  **Run the application**:
    ```bash
    ./run.sh
    ```
2.  **Controls**:
    - **Sensitivity**: Threshold for motion detection (Higher = less sensitive).
    - **Tile Size**: Grid granularity. Defaults to ~960x540. Smaller tiles = more sensitive to tiny area changes.
        - *Tip: Use Arrow Keys (Left/Right) to fine-tune sliders.*
    - **Capture on Keystroke**: Force capture a frame whenever a key is pressed (ideal for typing).
    - **FPS**: Maximum capture frequency.
    - **Quality**: JPEG compression quality.
    - **Output**: Select destination folder.
    - **Start/Stop**: Toggle recording.

## License
Freeware. Feel free to use and modify.
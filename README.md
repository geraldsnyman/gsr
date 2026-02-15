
# Simple Screen Recorder

A lightweight tool to capture screen activity as a sequence of high-quality JPEG images. Designed for creating coding tutorials, timelapses, and security monitoring where playback speed is determined in post-production.

## Features
- **Efficient Capture**: Only saves frames when significant change is detected.
- **Smart Sensitivity**: Grid-based detection (Tile Size) allows capturing small changes (like cursors) or ignoring them.
- **Keystroke Trigger**: Option to force capture when typing, ensuring no text is missed.
- **Adjustable Quality**: JPEG compression control to save space.
- **Persistant Settings**: Automatically saves and loads your configuration.
- **Modern UI**: Dark-themed, scrollable interface with keyboard support for sliders.
- **Linux Integration**: Includes desktop entry setup for system menu integration.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/geraldsnyman/ScreenRecorder.git
    cd ScreenRecorder
    ```

2.  **Run the automated setup script**:
    ```bash
    ./setup.sh
    ```
    *This script will:*
    - *Install necessary system dependencies (like `python3-tk`).*
    - *Create a Python virtual environment.*
    - *Install all required Python libraries from `requirements.txt`.*

3.  **(Optional) Install Desktop Entry (Linux)**:
    ```bash
    python3 setup_desktop.py
    ```
    *This allows you to find "Simple Screen Recorder" in your system's application menu and ensures the taskbar icon displays correctly.*

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

## Optimization Guide

To achieve the best balance of performance (low CPU) and capture accuracy:

1.  **Enable "Capture on Keystroke"**:
    -   This is the most efficient way to capture typing. It triggers a frame save *only* when you press a key, bypassing the need for intense visual scanning.
    -   With this on, you don't need small tiles to see text appear.

2.  **Start with "Large Tiles" (Slider to Left)**:
    -   Larger tiles (e.g., Full Screen or 960x540) require significantly less processing power than thousands of small tiles.
    -   Use this setting by default. Only move the slider right (smaller tiles) if you need to catch small visual changes *that don't involve typing* (like a specific icon changing color).

3.  **Tune Sensitivity (Threshold)**:
    -   **Sensitivity Slider** controls the "Noise Gate".
    -   **Lower Value (Left)** = Less Sensitive. Ignores small changes like cursor blinking or clock updates.
    -   **Higher Value (Right)** = More Sensitive. Captures almost everything.
    -   **Strategy**:
        -   Set Tile Size to **Large** (Left).
        -   Set Sensitivity to **Medium/High** (Center/Right).
        -   If it's missing big window changes, lower the Sensitivity (Left).
        -   If it's capturing too much (idle cursor blinking), increase Sensitivity (Right).

**Summary**: Use **Keystroke Capture** + **Large Tiles** + **Medium Sensitivity** for the most efficient recording of work/coding sessions.

## License
Freeware. Feel free to use and modify.
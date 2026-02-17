
# Simple Screen Recorder

A tool to capture your **Full 4K Desktop** as a smart sequence of high-quality JPEG images. 

Designed for the **"Capture Once, Edit Anywhere"** workflow: Record up to 4 applications (Code, Browser, Terminal, Live Preview) simultaneously on a 4K screen. In post-production (e.g., DaVinci Resolve), crop this single 4K master into multiple 1080p tracks to create a dynamic "multi-cam" editing experience without ever switching windows during recording.

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

1.  **Run the application (GUI)**:
    ```bash
    ./run.sh
    ```
2.  **Run via CLI (No GUI)**:
    ```bash
    python3 src/main.py --cli
    ```
    *Options:*
    - `--tiles <int>`: Override Tile Divisions (1 = Full Screen).
    - `--fps <val>`: Override FPS.
    - `--sens <val>`: Override Sensitivity.
    - `--keystroke`: Enable Capture on Keystroke.
    - `--mouse-click`: Enable Capture on Mouse Click.
    - `--mouse-scroll`: Enable Capture on Mouse Scroll.
    - `--mouse-move`: Enable Capture on Mouse Move.
    - `--show-cursor`: Draw Cursor Overlay on recording.
    - `--help`: Show all available options.

3.  **Controls**:
    - **Sensitivity**: Threshold for motion detection (Higher = less sensitive).
    - **Tile Size**: Grid granularity. Defaults to ~960x540. Smaller tiles = more sensitive to tiny area changes.
        - *Tip: Use Arrow Keys (Left/Right) to fine-tune sliders.*
    - **Triggers**:
        - **Keystroke**: Force capture on key press.
        - **Mouse**: Force capture on Click, Scroll, or Move.
    - **Cursor Overlay**: 
        - visually draws the mouse cursor (Dot, Target, Pointer) on the recording to ensure visibility.
        - customizable size (5-50px).
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
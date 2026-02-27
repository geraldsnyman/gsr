# Gerald's Screen Recorder (GSR)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![OS](https://img.shields.io/badge/os-linux-black)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI](https://img.shields.io/pypi/v/gsr.svg)

A tool to capture your **Full 4K Desktop** as a smart sequence of high-quality JPEG images.

GSR is a sensitivity-based motion and change recorder that intelligently monitors your screen. It only captures frames when a user-defined level of visual change occurs, or when specific keystroke and mouse activities are triggered, effectively eliminating dead footage and idle moments from your recordings.

## 🎨 App Icon

GSR's icon—a minimalist neon outline of a still camera body featuring a classic play button in place of the lens—perfectly encapsulates the core philosophy of the application. GSR captures your screen as a smart, optimized sequence of **still images** (represented by the camera body). However, because it intelligently records frames only when actual visual change occurs, these stills can be imported into Non-Linear Editing (NLE) software like DaVinci Resolve and instantly played back as a seamless, continuous **video sequence** (represented by the play button).

## ✨ Features

- **Capture Once, Edit Anywhere**: Record four applications simultaneously (code editor, browser, terminal, live preview) tiled on a single 4K screen. Crop this 4K master file in post-production into multiple 1080p tracks to create a dynamic "multi-cam" sequence.
- **Efficient Capture**: Only saves frames when the user-defined level of change is detected.
- **Smart Sensitivity**: Grid-based detection (Tile Size) allows capturing small changes (like cursors) or ignoring them.
- **Frame Rate**: Define a maximum capture speed (from 1 FPS up to 60 FPS) to maintain fluid motion without unnecessary overhead.
- **Keystroke Trigger**: Option to force capture when typing, ensuring no text is missed.
- **Mouse Trigger**: Option to force capture on mouse clicks, scrolls, or movements.
- **Adjustable Quality**: JPEG compression control to save space.
- **Persistent Settings**: Automatically saves and loads your configuration.
- **Modern UI**: Dark-themed, fixed window interface with keyboard support for sliders.
- **Linux Integration**: Includes desktop entry setup for system menu integration.

## 🚀 Installation

The stable release of `gsr` is available on [PyPI](https://pypi.org/project/gsr/).

Because `gsr` is a standalone command-line application, the highly recommended installation method is using **`pipx`**. This ensures the app is installed in an isolated environment without interfering with your system Python packages (especially important on Ubuntu 24.04 and other modern distributions enforcing PEP 668).

```bash
# 1. Install pipx (if you haven't already on Ubuntu/Debian)
sudo apt update && sudo apt install pipx
pipx ensurepath

# 2. Install gsr
pipx install gsr

# 3. (Optional) Install Linux Desktop integration + Icon
gsr --setup-desktop
```

To upgrade to the latest version in the future:
```bash
pipx upgrade gsr
```

### Alternative Installation methods

**(Optional) Standalone AppImage**: You can download the pre-compiled `GSR-x86_64.AppImage` directly from the [GitHub Releases](https://github.com/geraldsnyman/ScreenRecorder/releases) page.

**(Optional) Build from Source**:
If you want to contribute, test the app locally, or compile your own standalone AppImage binary:
```bash
git clone https://github.com/geraldsnyman/ScreenRecorder.git
cd ScreenRecorder
./scripts/setup.sh
python3 scripts/setup_desktop.py # (Optional) Install Desktop Entry for Linux
```

To run the application locally from the source code:
```bash
./scripts/run.sh
```

To build the standalone AppImage and PyPI packages yourself:
```bash
./scripts/release.sh
# The compiled binary will be located at: GSR-x86_64.AppImage
# The PyPI distribution files will be in: dist/
```

## 💻 Usage

### 1. GUI Mode
Simply run the application without any arguments to open the graphical interface:
```bash
gsr
# or locally:
./scripts/run.sh
```

### 2. CLI Mode
Providing any configuration flags will bypass the GUI and run headlessly:
```bash
gsr -f 30 -q 90 --keystroke --no-show-cursor
```

*Core Options:*
- `-h, --help`: Show program's help message and exit.
- `-v, --version`: Show program's version number and exit.
- `--setup-desktop`: Install Linux desktop entry and icon for system menu integration.
- `--save`: Save the provided CLI overrides to the permanent GUI settings.
- `-f, --fps <val>`: Override maximum FPS (1-60).
- `-s, --sens <val>`: Override Sensitivity (0-100).
- `-t, --tiles <val>`: Override Tile Divisions (1 = Full Screen).
- `-q, --quality <val>`: Override JPEG Output Quality (1-100).
- `-o, --output <path>`: Override Output Directory.

*Boolean Triggers (use `--feature` or `--no-feature`):*
- `--keystroke`: Force capture on key press.
- `--mouse-click`: Force capture on Mouse Click.
- `--mouse-scroll`: Force capture on Mouse Scroll.
- `--mouse-move`: Force capture on Mouse Move.
- `--show-cursor`: Draw Cursor Overlay on recording.

*Cursor Settings:*
- `--cursor-size <val>`: Override Cursor Size (5-50).
- `--cursor-style <style>`: Override Cursor Style (`dot`, `target`, `pointer`).

### 3. Controls & Workflow
- **Start/Stop**: Toggle recording using the GUI, or use `Ctrl + Z` in your terminal to pause (suspend) a CLI recording, `bg` to push it to the background, and `fg` to bring it back.
- **Sensitivity Controls**: Threshold for motion detection (Higher = more sensitive).
- **Tile Size**: Grid granularity. Defaults to ~960x540. Smaller tiles = more sensitive to tiny area changes. Use Arrow Keys (Left/Right) to fine-tune sliders.

## 🧠 Optimization Guide

To achieve the best balance of performance (low CPU) and capture accuracy:

1.  **Enable "Capture on Keystroke"**: The most efficient way to capture typing. It triggers a frame save *only* when you press a key, bypassing the need for intense visual scanning.
2.  **Start with "Large Tiles" (Slider to Left)**: Larger tiles (e.g., Full Screen or 960x540) require significantly less processing power than thousands of small tiles.
3.  **Tune Sensitivity (Threshold)**: 
    - Set Tile Size to **Large**.
    - Set Sensitivity to **Medium/High**.
    - If it's capturing too much idle blinking, lower the Sensitivity. If it's missing big window changes, increase the Sensitivity or reduce the Tile Size.

**Summary**: Use **Keystroke Capture** + **Large Tiles** + **Medium Sensitivity** for the most efficient recording of work/coding sessions.

## 📖 Documentation & Resources

*   [**Full Launch Plan & Architecture**](https://github.com/geraldsnyman/ScreenRecorder/blob/master/docs/LAUNCH_PLAN.md)
*   [**Issue Tracker**](https://github.com/geraldsnyman/ScreenRecorder/issues) - Report bugs or request features.

## 📝 License
Freeware. Feel free to use and modify.

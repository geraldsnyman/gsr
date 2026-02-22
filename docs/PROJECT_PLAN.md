# Gerald's Screen Recorder Project Plan

## 1. Objective: The 4K Multi-Track Workflow
This project is designed to enable a high-efficiency **"Capture Once, Edit Anywhere"** workflow while primarily **eliminating the recording of inactivity**.
- **The Concept**: Record the entire 4K desktop containing up to 4 full 1080p application windows (e.g., IDE, Browser, Terminal, Preview) simultaneously, capturing frames *only* when real activity occurs (e.g. typing, moving, rendering).
- **The Workflow**:
    1. **Recording**: Smart triggers (keystrokes, motion) ensure no dead footage is captured when thinking or stepping away.
    2. **Processing**: Run `ffmpeg` to split the raw 4K sequence into 4 distinct 1080p quadrant sequences.
    3. **Post-Production**: Import these 4 sequences into DaVinci Resolve for streamlined, virtual multi-cam editing.
- **The Goal**: Avoid tedious timeline scrubbing. An editor only sees active frames while no context is ever lost. Example: An edit in the IDE (View 1) causes an immediate update in the Browser (View 2). Both are captured perfectly in sync, with all the idle time squeezed out.

## 2. Core Philosophy
- **Resolution is King**: Primary output is high-bitrate, full-resolution JPEG sequences to ensure 1080p crops remain sharp.
- **Smart Efficiency**: Since recording full 4K at 60fps is data-heavy, we use **Smart Sensitivity** and **Keystroke Triggers** to only save frames when content actually changes.
- **Silent Reliability**: The recorder runs unobtrusively, ensuring that the "Purple Bar" or other artifacts do not ruin the clean capture of the workspace.

## 3. Technology Stack
- **Language**: Python 3.10+
- **GUI**: CustomTkinter
- **Capture**: `mss` (High performance) + `OpenCV` (Diffing)
- **Input**: `pynput` (Keystroke detection)

## 4. Project Structure
```
/
├── README.md               # User documentation
├── requirements.txt        # Python dependencies
├── setup.sh                # Automated installation script
├── run.sh                  # Execution script
├── setup_desktop.py        # Linux desktop entry generator
├── config.json             # Persistent settings (auto-generated)
├── assets/
│   └── icon.png            # Application Icon
├── src/
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── ui.py               # GUI implementation (CustomTkinter)
│   └── recorder.py         # Screen capture and processing logic
└── docs/
    ├── PROJECT_CHARTER.md  # High-level project vision
    └── PROJECT_PLAN.md     # This file
```

## 3. Core Features & Implementation Strategy
### A. Screen Capture Loop
- Use `mss` to grab the screen.
- run in a separate thread to keep UI responsive.

### B. Sensitivity (Motion Detection)
- Compare current frame with previous frame using `cv2.absdiff`.
- Calculate the percentage of changed pixels or average intensity difference.
- If difference > threshold (Sensitivity), save the frame.

### C. Frame Rate Control
- Use a timer or `time.sleep()` to limit the capture loop frequency based on user FPS setting.

### D. Optimization & Efficiency
- **Tile Alignment**: The "Tile Size" features uses doubling steps (powers of 2) to align grid boundaries with screen pixels where possible. This maximizes `cv2.resize` performance (INTER_AREA) by favoring integer downscaling factors.
- **Lazy Evaluation**: Change detection is performed before saving.

### E. Git Integration
- repo initialized.
- .gitignore configured for venv and recordings.

### F. Compression Control
- JPEG Quality adjustment (1-100%).
- Defaults to 100% for best quality.

### G. Directory Selection
- UI to browse and select output folder.
- Displays current path.

### H. Grid-Based Sensitivity (Tile Size) [Completed]
- Adjustable grid granularity.
- Granular control from Full Screen down to ~16px tiles.
- Automatic calibration based on screen resolution.
- **Optimization**: Defaults to ~960x540 tile size for balanced performance.

### I. Input-Triggered Capture [Completed]
- "Capture on Keystroke" option.
- Bypasses sensitivity threshold when keys are pressed, ensuring text entry is never missed.

### J. Linux Desktop Integration [Completed]
- Custom application icon.
- `setup_desktop.py` script to generate `.desktop` file for system integration.
- Proper Window Manager identity (WM_CLASS).

### K. Persistent Settings [Completed]
- Auto-save configuration (FPS, Sensitivity, Tile Size, etc.) to `config.json` on exit.
- Auto-load settings on startup.

### L. CLI Mode [Completed]
- Run headless mode automatically when configuration flags are provided.
- Override settings via flags (`-f`, `-s`, `-t`, `-o`, `--keystroke`, etc.).
- Include `--save` flag to persist CLI parameters to the GUI settings file.

### M. Mouse & Cursor Features [Completed]
- **Mouse Triggers**: Capture frames on Click, Scroll, or Move (optional).
- **Cursor Overlay**: Software-drawn cursor to fix Linux capture issues.
- **Customization**: Adjust cursor size (5-50px) and style (Dot, Target, Pointer).

## 4. Development Phases
- [x] **Phase 0: Initialization** - Setup project structure and docs.
- [x] **Phase 1: Core Logic** - Implement basic capture and save loop.
- [x] **Phase 2: Basic UI** - CTk interface for controls.
- [x] **Phase 3: Optimization** - Configurable FPS, Sensitivity, Quality.
- [x] **Phase 4: Advanced Features** - Smart Sensitivity (Tile Size), Keystroke Trigger.
- [x] **Phase 5: Refinement** - UI Polish (Scrollable), Linux Integration, Persistent Settings, CLI Support.
- [x] **Phase 6: Mouse & Cursor** - Click/Scroll/Move Triggers, Custom Cursor Overlay (Size/Style). 
- [x] **Phase 7: Testing & Polish** - Verify performance, docs (man pages, README), and UX.

## 5. Documentation Tasks
- Maintain README with usage instructions.
- Update this plan as features are completed.

## 6. Future Upgrades (Premium Roadmap)
- **Capture Card Integration**: Adding support for recording high-quality external video inputs directly into the workflow sequence.
- **DaVinci Resolve Automated Project Generator**: A post-production Python script that parses the recording metadata, creates a multi-track DaVinci Resolve timeline, imports the view tracks (quadrants), and automatically generates a master editing track that seamlessly switches between the views based on application activity and mouse location. This mimics the sophisticated behavior of an ATEM ISO directly on the software editing timeline.

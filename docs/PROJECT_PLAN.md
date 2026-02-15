# Simple Screen Recorder Project Plan

## 1. Objective: The 4K Multi-Track Workflow
This project is designed to enable a **"Capture Once, Edit Anywhere"** workflow.
- **The Concept**: Record the entire 4K desktop containing up to 4 full 1080p application windows (e.g., IDE, Browser, Terminal, Preview) simultaneously.
- **The Goal**: In post-production (e.g., DaVinci Resolve), the single 4K video source is duplicated into multiple tracks, each cropped to a specific 1080p region. This allows the editor to switch views (virtual multi-cam) between applications instantly without having to switch windows during the actual recording session.
- **Why**: This ensures no context is ever lost. Example: An edit in the IDE (View 1) causes an immediate update in the Browser (View 2). Both are captured perfectly in sync.

## 2. Core Philosophy
- **Resolution is King**: Primary output is high-bitrate, full-resolution JPEG sequences to ensure 1080p crops remain sharp.
- **Smart Efficiency**: Since recording full 4K at 60fps is data-heavy, we use **Smart Sensitivity** and **Keystroke Triggers** to only save frames when content actually changes.
- **Silent Reliability**: The recorder runs unobtrusively, ensuring that the "Purple Bar" or other artifacts do not ruin the clean capture of the workspace.

## 3. Technology Stack
- **Language**: Python 3.10+
- **GUI**: CustomTkinter
- **Capture**: `mss` (High performance) + `OpenCV` (Diffing)
- **Input**: `pynput` (Keystroke detection)

## 2. Project Structure
```
/
├── README.md               # User documentation
├── requirements.txt        # Python dependencies
├── src/
│   ├── main.py             # Entry point
│   ├── ui.py               # GUI implementation
│   ├── recorder.py         # Screen capture and processing logic
│   └── utils.py            # Helper functions
└── docs/
    ├── PROJECT_CHARTER.md  # High-level project definition
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

## 4. Development Phases
- [x] **Phase 0: Initialization** - Setup project structure and docs.
- [x] **Phase 1: Core Logic** - Implement basic capture and save loop.
- [x] **Phase 2: Basic UI** - CTk interface for controls.
- [x] **Phase 3: Optimization** - Configurable FPS, Sensitivity, Quality.
- [x] **Phase 4: Advanced Features** - Smart Sensitivity (Tile Size), Keystroke Trigger.
- [x] **Phase 5: Refinement** - UI Polish (Scrollable), Linux Integration, Persistent Settings.
- [ ] **Phase 4: Testing & Polish** - Verify performance and UX.

## 5. Documentation Tasks
- Maintain README with usage instructions.
- Update this plan as features are completed.

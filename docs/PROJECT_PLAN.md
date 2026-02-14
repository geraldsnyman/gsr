
# Project Plan: Simple Screen Recorder

## Overview.
This document outlines the development plan for the Simple Screen Recorder application. It will be maintained continuously to reflect the project's status, tech stack, and roadmap.

## 1. Technology Stack
- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter (Modern, dark-mode ready).
- **Screen Capture**: `mss` (Fast, cross-platform).
- **Image Processing**: `OpenCV` (for diffing/sensitivity) + `Pillow` (for saving).
- **Data Handling**: `numpy` (efficient array operations).

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

### E. Git Integration
- repo initialized.
- .gitignore configured for venv and recordings.

### F. Compression Control
- JPEG Quality adjustment (1-100%).
- Defaults to 100% for best quality.

## 4. Development Phases
- [x] **Phase 0: Initialization** - Setup project structure and docs.
- [x] **Phase 1: Core Logic** - Implement basic capture and save loop.
- [x] **Phase 2: UI Implementation** - Create the settings window and controls.
- [x] **Phase 3: Integration** - Connect UI to logic.
- [x] **Phase 3.5: Enhancements** - Git setup, Compression settings, Threading fixes.
- [ ] **Phase 4: Testing & Polish** - Verify performance and UX.

## 5. Documentation Tasks
- Maintain README with usage instructions.
- Update this plan as features are completed.

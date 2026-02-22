
# Project Charter: The Virtual Multi-Cam Recorder

## The Vision
To empower technical content creators with a tool that captures the **entire workspace context** at once. 
Instead of constantly switching scenes in OBS or sharing single windows, the creator records their **full 4K canvas** containing up to four 1080p applications (e.g., Code, Browser, Terminal, Live Preview).

The magic happens in **Post-Production** (e.g., DaVinci Resolve):
1.  **Process**: Use `ffmpeg` to split the single high-res Image Sequence into four distinct application quadrant sequences.
2.  **Edit**: Import these sequences into DaVinci Resolve.
3.  **Multi-Cam**: Edit using the sequences as a virtual multi-cam setup, switching between "angles" instantly.

## The Problem
Screen recording software often struggles with efficiency:
- **Record EVERYTHING**: The viewer sees tiny text on a 4K screen, and traditional recorders capture hours of **dead footage** (inactivity) when the user is thinking or steps away, requiring tedious editing.
- **Record ONE Window**: The viewer misses context updates happening in other windows (e.g., a browser refresh triggered by code save).

## The Solution
**Gerald's Screen Recorder** captures the full resolution but optimizes storage and the editor's time by using smart change detection (Sensitivity) and explicit input tracking (Keystrokes, Mouse). It acts as an intelligent camera that **eliminates the recording of inactivity**. It delivers a continuous "Master Tape" of your active session. From this master tape, any specific "Camera Angle" (Application View) can be extracted in perfect 1080p clarity without forcing the editor to scrub through hours of nothingness.

## Scope
### In-Scope
- Screen capture via `mss`.
- Change detection algorithm (sensitivity).
- Adjustable Frame Rate (FPS).
- Input Triggers (Keystroke, Mouse Click/Scroll/Move).
- Cursor Overlay with customizable Styles.
- Basic GUI for settings and control.

### Out-of-Scope (for MVP)
- Audio recording.
- Video encoding (output is image sequence).
- Built-in playback or editing features.
- Multi-monitor support beyond primary screen (initially).

### Future Upgrades (Premium Tier)
- **Capture Card Integration**: Support high-quality video inputs alongside the screen recording.
- **DaVinci Resolve Project Generator**: An automation script that builds a Resolve project with the quadrant sequences and a master track that automatically switches views based on activity or mouse position (similar to an ATEM ISO workflow).

## Stakeholders
- **Content Creators / Educators**: Need extreme multi-cam flexibility for software or physical tutorials, while avoiding recording dead footage (e.g., waiting between keystrokes or actions).
- **Developers / Tech Teams**: Need to record flawless bug reproductions without exposing the underlying desktop or other sensitive background applications.
- **Developer**: GSVV and Antigravity (AI).

## Deliverables
- Source code (Python).
- Executable/Runnable script.
- Documentation (README, Project Plan).

## Constraints
- Must be functional by end of day 2026-02-14.
- Must run on Linux (user's OS).

## Risks
- Performance issues with high frame rates or high resolution.
- Disk space usage for long recordings.

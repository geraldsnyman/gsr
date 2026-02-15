
# Project Charter: The Virtual Multi-Cam Recorder

## The Vision
To empower technical content creators with a tool that captures the **entire workspace context** at once. 
Instead of constantly switching scenes in OBS or sharing single windows, the creator records their **full 4K canvas** containing up to four 1080p applications (e.g., Code, Browser, Terminal, Live Preview).

The magic happens in **Post-Production** (e.g., DaVinci Resolve):
1.  Import the single high-res Image Sequence.
2.  Duplicate the track 4 times.
3.  Crop each track to a specific application quadrant.
4.  Switch between these "angles" instantly.

## The Problem
Screen recording software often forces a choice:
- **Record EVERYTHING**: The viewer sees tiny text on a 4K screen.
- **Record ONE Window**: The viewer misses context updates happening in other windows (e.g., a browser refresh triggered by code save).

## The Solution
**Simple Screen Recorder** captures the full resolution but optimizes storage using smart change detection (Sensitivity + Keystrokes). It delivers a "Master Tape" of your entire session, from which any specific "Camera Angle" (Application View) can be extracted in perfect 1080p clarity later.

## Scope
### In-Scope
- Screen capture via `mss`.
- Change detection algorithm (sensitivity).
- Adjustable Frame Rate (FPS).
- Output to a designated folder.
- Basic GUI for settings and control.

### Out-of-Scope
- Audio recording.
- Video encoding (output is image sequence).
- Built-in playback or editing features.
- Multi-monitor support beyond primary screen (initially).

## Stakeholders
- **User**: Content creators, developers, security monitoring.
- **Developer**: Antigravity (AI).

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

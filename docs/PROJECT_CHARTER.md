
# Project Charter: Simple Screen Recorder

## Project Title
Simple Screen Recorder

## Problem Statement
There is a need for a lightweight, simple tool to capture screen activity as a sequence of images (.jpg) rather than a video file. This allows for flexible post-production (e.g., in DaVinci Resolve) where playback rate can be determined later. Existing tools often focus on video output or lack specific features like sensitivity-based capture.

## Objectives
- Develop a Python-based desktop application.
- Capture screen content and save as a sequence of .jpg images.
- Implement "sensitivity" adjustment to minimize storage by only saving frames with significant changes.
- Allow user-configurable capture frame rate.
- Ensure the application is performant and easy to use.

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

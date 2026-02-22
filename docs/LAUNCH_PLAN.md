# Launch & Marketing Plan: Gerald's Screen Recorder (GSR)

This document outlines the strategy for releasing, distributing, and promoting Gerald's Screen Recorder (GSR) to the developer and creator community.

## 1. Objectives
- **Establish Presence**: Launch minimal viable product (MVP) as a trusted, open-source tool.
- **Drive Adoption**: Get developers and content creators to try the tool.
- **Build Community**: Encourage feedback, contributions, and word-of-mouth.
- **Monetization (Long-term)**: Create a funnel from free users to potential premium services, such as capture card support and advanced post-production automation scripts.

### Target Audience & Core Purpose
The primary purpose of this screen recorder is to **eliminate the recording of inactivity**. It intelligently captures only when necessary, avoiding dead footage when the user is thinking or steps away.
- **Content Creators / Educators**: Ideal for creating tutorials. Perfect for excessive typing tutorials (e.g., coding or writing) by capturing each keystroke as a frame, or for action tutorials (e.g., carpentry) where motion sensitivity skips over idle moments.
- **Developers/Tech Teams**: Professionals needing an efficient way to record bug reproductions without capturing their entire cluttered desktop or exposing sensitive background apps.

### Typical Post-Production Workflow
For tutorials utilizing a "split-screen" layout (e.g., a screen divided into quadrants for a code editor, web browser, file browser, and terminal):
1. **Processing**: Use `ffmpeg` to split the raw recorded sequence into distinct quadrant sequences.
2. **Editing**: Import these split sequences into DaVinci Resolve for multi-cam editing. (Alternatively, raw recordings can be split into quadrants directly within DaVinci Resolve with some extra effort).

### Future Upgrades (Premium Tier)
- **Capture Card Integration**: Support for recording video inputs via capture cards to ensure much higher video quality.
- **DaVinci Resolve Project Generator**: A script that creates a DaVinci Resolve project with a multi-track timeline for each view. It will feature a master track that automatically switches between views based on mouse position or active window (e.g., typing in Antigravity makes that view live; switching to the web browser automatically cuts to the browser). This mimics the automated multi-cam workflow of an ATEM ISO.

### Success Metrics (First 30 Days)
- **GitHub**: 100+ Stars, 10+ Forks.
- **Distribution**: 500+ Downloads/Installs.
- **Content**: 1,000+ Views on the YouTube launch video.
- **Community**: At least 5 user-submitted issues or feature requests.

## 2. Pre-Launch Checklist (Technical)

### A. Branding & Polish
- [x] **Rebranding**: Rename to "Gerald's Screen Recorder" (GSR). Update executable/CLI to `gsr`.
- [x] **UI Review**: Verify the user interface is visually pleasing, intuitive, and clearly structured.
- [x] **CLI Verification**: Ensure CLI flags are comprehensive, logical, and consistently named.

### B. Documentation Completeness
- [x] **Core Docs**: README, Contributing Guide, License.
- [x] **Project Documents**: Project Charter, Project Plan, Packing Guide, and Launch Plan.
- [x] **CLI Manuals**: Ensure `gsr --help` output is highly detailed and generate a formal Linux `man` page.
- [x] **Wiki / Extended Docs**: Ensure `.md` files are current and prepared for a potential GitHub Wiki.

### C. Packaging & Distribution
- [x] **Action**: Setup `pyproject.toml` for PyPI publishing (`pipx install gsr`).
- [x] **Action**: Investigate/Build `AppImage` for universal Linux distribution.
- [x] **Action**: Create a `release.sh` script to automate packaging & PyPI upload.

### D. Testing
- [x] **Test**: Verify on a fresh Linux install (Options: VM, Live USB, Docker).
- [x] **Test**: PyPI installation in an isolated virtual environment.
- [x] Test long recording sessions (1hr+).


## 3. Release Phase (Distribution)
### A. GitHub Repository (The Hub)
- [x] **Action**: Polish the Repo. Use a clean description, tags (`screen-recorder`, `python`, `linux`, `open-source`, `creator-tools`).
- [ ] **Release Assets**: Upload the `AppImage` or `zip` of source code to the "Releases" section.
- [x] **Badges**: Add build status, license, and version badges to README.

### B. Website (The Storefront - gsvv.co.za)
- [ ] **Landing Page**: Create `gsvv.co.za/software/gsr`.
    - [ ] **Hero Section**: "The Professional's Layout Recorder. Capture Context, Crop Later."
    - [ ] **Download Button**: Direct link to the `AppImage` or GitHub Release.
    - [ ] **Feature Highlight**: Show the "Multi-Track Workflow" concept visually.
    - [ ] **Tutorial**: Embed the YouTube tutorial here.

### C. Package Managers (Optional/Future)
- [ ] **PyPI (pip)**: `pip install simple-screen-recorder` (Good for devs).
- [ ] **Snap/Flatpak**: Consider later for wider Linux store reach.

## 4. Marketing Strategy (Promotion)
### A. Content Marketing (YouTube)
- [ ] **Video 1: The "Why" (Concept)**: "Stop Switching Windows! How I Record 4 Apps at Once."
    - [ ] Demonstrate the problem (context switching).
    - [ ] Show the solution (4K capture -> 1080p crops in DaVinci Resolve).
- [ ] **Video 2: The "How" (Tutorial)**: "Simple Screen Recorder: Full Walkthrough."
    - [ ] Installation.
    - [ ] configuration (Sensitivity, Tiles, Triggers).
    - [ ] The CLI workflow for automation.

### B. Developer & Maker Communities
- [ ] **Reddit**: Post in `r/linuxapps`, `r/python`, `r/contentcreation`, `r/software`.
    - [ ] *Title Idea*: "I built a screen recorder specifically for multi-track editing workflows. It's open source."
- [ ] **Hacker News**: Show HN the tool. Focus on the technical aspect ("Smart Sensitivity", "Python/OpenCV").
- **Product Hunt**: Launch page for broader tech audience.
    - *Prep*: Create an animated GIF of the workflow, prepare the "Maker Comment" explaining why we built it, and schedule the launch.

### C. Social Media
- **Twitter/X**: Share short clips of the "Crop Workflow" with `#buildinpublic` `#opensource`.
- **LinkedIn**: Professional announcement connecting to the GSVV brand, highlighting productivity benefits.

## 5. Post-Launch & Maintenance
- **Monitor Issues**: Respond to GitHub Issues within 48h to build trust.
- **Update Cycle**: Aim for a cadence (e.g., monthly fixes or features).
- **User Feedback**: Add a "Feedback" link in the app (or simple `mailto`).
- **Roadmap**: Keep `PROJECT_PLAN.md` public so users see activity.

## 6. Action Plan
| Timeline | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Day 1** | Finalize Code & Docs. Create GitHub Repo. | Dev | In Progress |
| **Day 2** | Build AppImage/Binary. Test on clean machine. | Dev | Pending |
| **Day 3** | Record & Edit "Concept" Video. | Creator | Pending |
| **Day 4** | Build Landing Page on `gsvv.co.za`. | Web Dev | Pending |
| **Day 5** | **LAUNCH**: Push to GitHub, Publish Video, Post on Reddit/HN. | All | Pending |
| **Day 7** | Review Feedback, Fix Critical Bugs. | Dev | Pending |


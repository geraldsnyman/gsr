# Launch & Marketing Plan: Simple Screen Recorder

This document outlines the strategy for releasing, distributing, and promoting Simple Screen Recorder (SSR) to the developer and creator community.

## 1. Objectives
- **Establish Presence**: Launch minimal viable product (MVP) as a trusted, open-source tool.
- **Drive Adoption**: Get developers and content creators to try the tool.
- **Build Community**: Encourage feedback, contributions, and word-of-mouth.
- **Monetization (Long-term)**: Create a funnel from free users to potential premium services (cloud, backup, etc.).

## 2. Pre-Launch Checklist (Technical)
- [x] **Code Complete**: MVP features (Capture, Mouse/Key Triggers, UI, CLI) are stable.
- [x] **Documentation**: README, Contributing Guide, License.
- [ ] **Packaging**:
    - [ ] Create a `.desktop` installer script (done).
    - [ ] **Action**: Investigate/Build `AppImage` for universal Linux distribution (avoids dependency hell).
    - [ ] **Action**: Create a `release.sh` script to automate packaging.
- [ ] **Testing**:
    - [ ] Verify on a fresh Linux install (VM or clean environment).
    - [ ] Test long recording sessions (1hr+).

## 3. Release Phase (Distribution)
### A. GitHub Repository (The Hub)
- **Action**: Polish the Repo. Use a clean description, tags (`screen-recorder`, `python`, `linux`, `open-source`, `creator-tools`).
- **Release Assets**: Upload the `AppImage` or `zip` of source code to the "Releases" section.
- **Badges**: Add build status, license, and version badges to README.

### B. Website (The Storefront - gsvv.co.za)
- **Landing Page**: Create `gsvv.co.za/software/screen-recorder`.
    - **Hero Section**: "The Professional's Layout Recorder. Capture Context, Crop Later."
    - **Download Button**: Direct link to the `AppImage` or GitHub Release.
    - **Feature Highlight**: Show the "Multi-Track Workflow" concept visually.
    - **Tutorial**: Embed the YouTube tutorial here.

### C. Package Managers (Optional/Future)
- **PyPI (pip)**: `pip install simple-screen-recorder` (Good for devs).
- **Snap/Flatpak**: Consider later for wider Linux store reach.

## 4. Marketing Strategy (Promotion)
### A. Content Marketing (YouTube)
- **Video 1: The "Why" (Concept)**: "Stop Switching Windows! How I Record 4 Apps at Once."
    - Demonstrate the problem (context switching).
    - Show the solution (4K capture -> 1080p crops in DaVinci Resolve).
- **Video 2: The "How" (Tutorial)**: "Simple Screen Recorder: Full Walkthrough."
    - Installation.
    - configuration (Sensitivity, Tiles, Triggers).
    - The CLI workflow for automation.

### B. Developer Communities
- **Reddit**: Post in `r/linuxapps`, `r/python`, `r/contentcreation`, `r/software`.
    - *Title Idea*: "I built a screen recorder specifically for multi-track editing workflows. It's open source."
- **Hacker News**: Show HN the tool. Focus on the technical aspect ("Smart Sensitivity", "Python/OpenCV").
- **Product Hunt**: Launch page for broader tech audience.

### C. Social Media
- **Twitter/X**: Share short clips of the "Crop Workflow" with `#buildinpublic` `#opensource`.
- **LinkedIn**: Professional announcement connecting to the GSVV brand.

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


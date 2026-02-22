# Application Packaging Guide

This document outlines how Gerald's Screen Recorder (GSR) is bundled from raw source code into a single, distributable application (AppImage or PyPI package).

## Do We Need a specific "Packing List"?
The short answer is **no, but we have configuration files that act like one.** 
Modern Python packaging tools are smart. They don't look at your folder and try to package *everything*. Instead, they look at your main entry point (`src/main.py`) and mathematically trace every single `import` statement. They only grab the exact Python code required to run the app. 

Therefore, things like `docs/`, `scratch/`, test animations, or the `recordings/` folder are completely ignored by default! 

However, since the packager only auto-detects *code*, we must explicitly tell it to include "data files" (like your `assets/icon.png`). This configuration file serves as our "packing list."

---

## Method 1: The AppImage (For the standard user)
*An AppImage is a single file that contains your entire app and all of its dependencies. A user just downloads it, double-clicks it, and it runs on almost any Linux distribution.*

### Step 1: Bundling the Python Code (PyInstaller)
We use a tool called `PyInstaller`. 
1. We run `pyinstaller --onefile src/main.py`.
2. PyInstaller traces all the code, bundles the Python interpreter, OpenCV, CustomTkinter, and your code into one massive, standalone binary file.
3. **The Packing List (`main.spec`)**: PyInstaller creates a `.spec` file. We edit this file to tell it: *"Hey, also bundle the `assets/` folder inside the binary so the app has its icon!"*

### Step 2: Creating the AppImage
Once PyInstaller creates a working standalone Linux binary, we convert that into an AppImage.
1. We create a directory structure called an `AppDir`.
2. We place our compiled binary, our `.desktop` file, and an icon inside this directory.
3. We use a tool called `appimagetool` which compresses this `AppDir` into a single `.AppImage` file.

---

## Method 2: PyPI (For Developers via `pip` or `pipx`)
*This allows Linux developers to simply run `pipx install gsr` in their terminal.*

### Step 1: The `pyproject.toml` File (The standard Packing List)
We create a file in the root directory called `pyproject.toml`. This file defines the app's name, version, author, and states that the `src/` folder contains the actual application. 

### Step 2: The `MANIFEST.in` File (The Data Packing List)
If we need to include non-code files (like the `README.md` or a license), we create a `MANIFEST.in` file. We can explicitly write `prune docs/` or `exclude scratch/*` here just to be universally safe, but it's usually not necessary if the `pyproject.toml` only points to `src/`.

### Step 3: Building & Uploading
We run `python -m build`. This creates a `.tar.gz` (Source Archive) and a `.whl` (Wheel/Compiled Archive) file inside a `dist/` folder. We securely upload these files to PyPI (Python Package Index) using a tool called `twine`.

---

## Next Steps
To begin packaging right now, we should:
1. Initialize the **PyInstaller** process to generate the `.spec` file.
2. Draft a `release.sh` bash script to automatically execute the whole PyInstaller -> AppImage pipeline so you never have to do it manually. 

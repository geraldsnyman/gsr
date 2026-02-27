#!/bin/bash

# release.sh
# Automates the building of the PyPI package and the standalone Linux AppImage

cd "$(dirname "$0")/.." || exit

echo "=== Packaging Gerald's Screen Recorder ==="

# Ensure virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# 1. BUILD PyPI PACKAGE (Wheel & Source distribution)
echo "--- Building PyPI Package ---"
pip install --upgrade build twine
python3 -m build
echo "PyPI build complete. Artifacts are in dist/"

# 2. BUILD SINGLE BINARY via PyInstaller
echo "--- Building Standalone Binary via PyInstaller ---"
pip install pyinstaller
mkdir -p bin
pyinstaller --name gsr --onefile --noconfirm --distpath bin src/main.py
echo "PyInstaller build complete. Binary is at bin/gsr."

# 3. BUILD APPIMAGE
echo "--- Building AppImage ---"

# Setup AppDir structure
APPDIR="build/AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"

# Copy binary
cp bin/gsr "$APPDIR/usr/bin/gsr"

# Copy Icon
cp assets/icon.png "$APPDIR/gsr.png"

# Create Desktop Entry for AppImage
cat <<EOF > "$APPDIR/gsr.desktop"
[Desktop Entry]
Name=Gerald's Screen Recorder
Exec=gsr
Icon=gsr
Type=Application
Categories=Utility;Video;AudioVideo;
EOF

# Create AppRun script
cat <<'EOF' > "$APPDIR/AppRun"
#!/bin/sh
APPDIR=$(dirname "$(readlink -f "$0")")
exec "$APPDIR/usr/bin/gsr" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Download appimagetool if not exists
if [ ! -f "appimagetool" ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -O appimagetool
    chmod +x appimagetool
fi

# Generate the AppImage
ARCH=x86_64 ./appimagetool "$APPDIR" GSR-x86_64.AppImage

echo "=== Build Complete! ==="
echo "PyPI Installable Wheel : dist/"
echo "Standalone AppImage    : GSR-x86_64.AppImage"

# 4. AUTOMATED GITHUB RELEASE
if [ "$1" == "--publish" ]; then
    if command -v gh &> /dev/null; then
        echo "--- Creating/Updating GitHub Release ---"
        VERSION=$(grep -m 1 '^version = ' pyproject.toml | cut -d '"' -f 2)
        TAG="v$VERSION"
        
        # Check if the release already exists
        if gh release view "$TAG" >/dev/null 2>&1; then
            echo "Release $TAG already exists. Uploading AppImage binary..."
            gh release upload "$TAG" GSR-x86_64.AppImage --clobber
        else
            echo "Creating new release $TAG..."
            # If the tag doesn't exist locally/remotely, gh will automatically create it
            gh release create "$TAG" GSR-x86_64.AppImage --title "GSR $TAG" --generate-notes
        fi
        echo "GitHub Release process complete! Check it at: https://github.com/geraldsnyman/gsr/releases"
    else
        echo "GitHub CLI (gh) not found. Skipping automated GitHub release."
    fi
else
    echo "--- Notice ---"
    echo "Skipping automated GitHub Release."
    echo "If you are the repository owner, run './scripts/release.sh --publish' to automatically upload to GitHub."
fi

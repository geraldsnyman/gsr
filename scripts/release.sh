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


#!/bin/bash

# Setup script for Gerald's Screen Recorder (GSR)

cd "$(dirname "$0")/.." || exit

echo "Checking system dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        echo "Installing python3-tk and scrot via apt-get (needs sudo)..."
        sudo apt-get update
        sudo apt-get install -y python3-tk python3-dev scrot
    elif command -v dnf &> /dev/null; then
        echo "Installing python3-tkinter via dnf (needs sudo)..."
        sudo dnf install -y python3-tkinter
    else
        echo "Warning: Could not detect package manager. Please ensure python3-tk is installed."
    fi
else
    echo "OS is $OSTYPE. Assuming non-Linux or manual installation."
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate and install requirements
echo "Activating venv and installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete. Run ./run.sh to start the recorder."


#!/bin/bash

# Run script for Gerald's Screen Recorder (GSR)

cd "$(dirname "$0")/.." || exit

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh..."
    ./scripts/setup.sh
fi

source venv/bin/activate
python src/main.py "$@"

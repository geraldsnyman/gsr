
#!/bin/bash

# Run script for Gerald's Screen Recorder (GSR)

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh..."
    ./setup.sh
fi

source venv/bin/activate
python src/main.py "$@"

#!/bin/bash
# Script to run the Icelandic TTS and STT tests

# Create virtual environment if it doesn't exist
if [ ! -d "icelandic-env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv icelandic-env
fi

# Activate virtual environment
source icelandic-env/bin/activate

# Run the test suite
python run_icelandic_tests.py "$@"

# Deactivate virtual environment
deactivate

echo "Tests complete!"
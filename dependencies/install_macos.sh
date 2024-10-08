#!/bin/bash

# Function to install PyAudio using pip
install_pyaudio() {
    python3 -m pip install pyaudio
    echo "PyAudio installed successfully!"
}

# Check for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    echo "Installing dependencies for macOS..."
    brew install portaudio

    # Now install PyAudio using pip
    install_pyaudio
else
    echo "This script is intended for macOS only."
    exit 1
fi

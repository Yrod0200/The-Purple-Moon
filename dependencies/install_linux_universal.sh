#!/bin/bash
echo "\033[0;····················································";
echo ": ███████████ █████                                :";
echo ":░█░░░███░░░█░░███                                 :";
echo ":░   ░███  ░  ░███████    ██████                   :";
echo ":    ░███     ░███░░███  ███░░███                  :";
echo ":    ░███     ░███ ░███ ░███████                   :";
echo ":    ░███     ░███ ░███ ░███░░░                    :";
echo ":    █████    ████ █████░░██████                   :";
echo ":   ░░░░░    ░░░░ ░░░░░  ░░░░░░                    :";
echo ":                                                  :";
echo ":                                                  :";
echo ":                                                  :";
echo ": ███████████                       ████           :";
echo ":░░███░░░░░███                     ░░███           :";
echo ": ░███    ░███ █████ ████ ████████  ░███   ██████  :";
echo ": ░██████████ ░░███ ░███ ░░███░░███ ░███  ███░░███ :";
echo ": ░███░░░░░░   ░███ ░███  ░███ ░███ ░███ ░███████  :";
echo ": ░███         ░███ ░███  ░███ ░███ ░███ ░███░░░   :";
echo ": █████        ░░████████ ░███████  █████░░██████  :";
echo ":░░░░░          ░░░░░░░░  ░███░░░  ░░░░░  ░░░░░░   :";
echo ":                         ░███                     :";
echo ":                         █████                    :";
echo ":                        ░░░░░                     :";
echo ": ██████   ██████                                  :";
echo ":░░██████ ██████                                   :";
echo ": ░███░█████░███   ██████   ██████  ████████       :";
echo ": ░███░░███ ░███  ███░░███ ███░░███░░███░░███      :";
echo ": ░███ ░░░  ░███ ░███ ░███░███ ░███ ░███ ░███      :";
echo ": ░███      ░███ ░███ ░███░███ ░███ ░███ ░███      :";
echo ": █████     █████░░██████ ░░██████  ████ █████     :";
echo ":░░░░░     ░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░      :";
echo "····················································\033[0m";

# Function to install PyAudio using pip
install_pyaudio() {
    python3 -m pip install pyaudio
    python3 -m pip install pyaes
    echo "PyAudio installed successfully!"
}

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Detected distribution: $NAME"

    case $ID in
        ubuntu|debian)
            echo "Installing dependencies for Debian/Ubuntu..."
            sudo apt-get update
            sudo apt-get install -y python3-pyaudio python3-pyaes
            install_pyaudio
            ;;
        fedora)
            echo "Installing dependencies for Fedora..."
            sudo dnf install -y python3-pyaudio python3-pyaes
            install_pyaudio
            ;;
        arch)
            echo "Installing dependencies for Arch Linux..."
            sudo pacman -S --noconfirm python-pyaudio python3-pyaes
            install_pyaudio
            ;;
        centos|rhel)
            echo "Installing dependencies for CentOS/RHEL..."
            sudo yum install -y python3-pyaudio python3-pyaes
            install_pyaudio
            ;;
        *)
            echo "Unsupported distribution. Please try to install PyAudio manually."
            exit 1
            ;;
    esac
else
    echo "Could not detect the Linux distribution."
    exit 1
fi

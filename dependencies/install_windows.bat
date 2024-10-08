@echo off
set /p confirm="Would you like to install the requiriments? Only respond with: (y/n): "

if /i "%confirm%"=="y" (
    python -m pip install pyaudio
    echo PyAudio instalado com sucesso.
) else (
    echo Instalação cancelada.
)
pause

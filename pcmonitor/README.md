# PCMonitor

A simple desktop app to monitor CPU and RAM usage in real time using a graphical interface.

## Features
- Displays CPU and RAM usage
- Responsive UI (font size adjusts with window size)
- Exit button for graceful shutdown
- Error handling for missing dependencies
- Code structured for maintainability
- Placeholder for minimize-to-tray feature

## Requirements
- Python 3.7+
- Tkinter (install via your system package manager)
- psutil (install via pip)

## Setup
1. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```sh
   pip install psutil
   ```
3. **Install Tkinter:**
   - On Manjaro/Arch:
     ```sh
     sudo pacman -S tk
     ```
   - On Ubuntu/Debian:
     ```sh
     sudo apt-get install python3-tk
     ```

## Usage
Run the app with:
```sh
python pcmon.py
```

## Notes
- For minimize-to-tray support, additional packages (e.g., pystray) may be required in future updates.
- If you see a warning about missing modules, ensure your virtual environment is activated and dependencies are installed.

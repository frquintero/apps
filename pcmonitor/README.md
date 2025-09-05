# PCMonitor

A feature-rich desktop app to monitor CPU and RAM usage in real time with a modern graphical interface.

## Features
- **Real-time monitoring** of CPU and RAM usage with configurable refresh rate
- **System tray support** - minimize to tray and restore from tray
- **Customizable UI** - change colors, refresh rate, and display options
- **System information** - detailed CPU, memory, and disk usage information
- **Responsive design** - font size automatically adjusts to window size
- **Configuration persistence** - settings saved between sessions
- **Menu bar** with File, View, and Help menus
- **Data history tracking** - keeps last 60 readings for potential graphing
- **Cross-platform** - works on Windows, Linux, and macOS
- **Graceful error handling** with user-friendly messages

## Requirements
- Python 3.7+
- Tkinter (usually included with Python)
- psutil (install via pip)

### Optional (for system tray support)
- pystray and pillow (install via pip)

## Installation

### Quick Install (with system tray support)
```bash
pip install psutil pystray pillow
python pcmon.py
```

### Basic Install (no system tray)
```bash
pip install psutil
python pcmon.py
```

### System-specific Tkinter installation
If you get Tkinter errors:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Manjaro/Arch:**
```bash
sudo pacman -S tk
```

**Windows:**
Tkinter is usually included with Python. If not, reinstall Python and ensure "tcl/tk and IDLE" is selected.

## Usage

### Basic Usage
```bash
python pcmon.py
```

### Command Line Options
The application accepts an optional refresh rate parameter:
```bash
python pcmon.py 2000  # Update every 2 seconds
```

### Interface Guide
- **Main Display**: Shows CPU and RAM usage percentages
- **Menu Bar**: Access settings, view options, and help
- **Buttons**:
  - ⬇ Tray: Minimize to system tray (if available)
  - ⚙ Settings: Open settings dialog
  - ❌ Exit: Close application with confirmation

### Settings
- **Refresh Rate**: Adjust update frequency (100-10000ms)
- **Colors**: Customize background and text colors
- **System Info**: Toggle additional system information display

## Configuration
Settings are automatically saved to `~/.pcmonitor_config.json` and include:
- Window size and position
- Color preferences
- Refresh rate
- Display preferences

## Advanced Features

### System Tray
When pystray is installed, you can:
- Minimize the app to system tray
- Right-click tray icon to show/exit
- App continues monitoring while minimized

### System Information
Access detailed system info including:
- CPU core count and frequency
- Total/available memory
- Disk usage statistics

### Error Handling
- Graceful handling of missing dependencies
- User-friendly error messages
- Automatic fallback options

## Troubleshooting

### "tkinter not found"
Install tkinter for your operating system (see System-specific installation above).

### "psutil not found"
Install with: `pip install psutil`

### System tray not working
Install optional dependencies: `pip install pystray pillow`

### App won't start
Check Python version (3.7+ required) and ensure all dependencies are installed.

## Development

### Code Structure
- `PCMonitorApp` class handles the main application
- Configuration management with JSON persistence
- Thread-safe system tray implementation
- Modular design for easy extension

### Extending the Application
- Add new monitoring metrics by extending the `update()` method
- Create new menu items in `create_menu()`
- Add configuration options to the settings dialog

## License
This project is open source and available under the MIT License.

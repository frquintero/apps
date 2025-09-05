
import tkinter as tk
from tkinter import messagebox, simpledialog
import psutil
import threading
import time
from datetime import datetime
import platform
import os
import json
from pathlib import Path

# Try to import system tray functionality
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("Note: pystray not available. Install with 'pip install pystray pillow' for system tray support.")

class PCMonitorApp:
    def __init__(self, refresh_rate=1000):
        self.config_file = Path.home() / '.pcmonitor_config.json'
        self.config = self.load_config()
        
        self.root = tk.Tk()
        self.root.title("💻 PC Monitor")
        self.root.geometry(self.config.get('window_size', '600x300'))
        self.root.configure(bg=self.config.get('bg_color', 'black'))
        self.root.minsize(300, 150)
        self.root.bind('<Configure>', self.on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create menu bar
        self.create_menu()
        
        # Main display label
        self.lbl = tk.Label(
            self.root, 
            font=("Arial", 30, "bold"), 
            bg=self.config.get('bg_color', 'black'), 
            fg=self.config.get('fg_color', 'lime')
        )
        self.lbl.pack(expand=True, fill='both')
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.config.get('bg_color', 'black'))
        button_frame.pack(side="bottom", pady=10)
        
        # Minimize to tray button
        if TRAY_AVAILABLE:
            self.tray_btn = tk.Button(
                button_frame, 
                text="⬇ Tray", 
                command=self.minimize_to_tray, 
                font=("Arial", 12), 
                bg="blue", 
                fg="white"
            )
            self.tray_btn.pack(side="left", padx=5)
        
        # Settings button
        self.settings_btn = tk.Button(
            button_frame, 
            text="⚙ Settings", 
            command=self.open_settings, 
            font=("Arial", 12), 
            bg="gray", 
            fg="white"
        )
        self.settings_btn.pack(side="left", padx=5)
        
        # Exit button
        self.exit_btn = tk.Button(
            button_frame, 
            text="❌ Exit", 
            command=self.on_closing, 
            font=("Arial", 12), 
            bg="red", 
            fg="white"
        )
        self.exit_btn.pack(side="left", padx=5)
        
        # Data storage for history
        self.cpu_history = []
        self.ram_history = []
        self.max_history = 60  # Keep last 60 readings
        
        self.refresh_rate = self.config.get('refresh_rate', refresh_rate)
        self.tray_icon = None
        self.is_minimized_to_tray = False
        
        self.update()

    def update(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            
            # Store history
            current_time = datetime.now().strftime("%H:%M:%S")
            self.cpu_history.append((current_time, cpu))
            self.ram_history.append((current_time, ram))
            
            # Keep only recent history
            if len(self.cpu_history) > self.max_history:
                self.cpu_history.pop(0)
            if len(self.ram_history) > self.max_history:
                self.ram_history.pop(0)
            
            # Create display text with additional info
            display_text = f"💻 CPU Usage: {cpu:.1f}%\n💾 RAM Usage: {ram:.1f}%"
            
            # Add system info if enabled
            if self.config.get('show_system_info', True):
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:
                    display_text += f"\n⚡ CPU Freq: {cpu_freq.current:.0f}MHz"
                
                # Add memory details
                memory = psutil.virtual_memory()
                display_text += f"\n📊 Available: {memory.available // (1024**3):.1f}GB"
            
            self.lbl.config(text=display_text)
            
        except Exception as e:
            self.lbl.config(text=f"❌ Error: {str(e)}")
        
        self.root.after(self.refresh_rate, self.update)

    def on_resize(self, event):
        # Responsive font size based on window height
        new_size = max(12, int(event.height / 10))
        self.lbl.config(font=("Arial", new_size, "bold"))

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle System Info", command=self.toggle_system_info)
        view_menu.add_command(label="Reset Window Size", command=self.reset_window_size)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="System Info", command=self.show_system_info)

    def load_config(self):
        """Load configuration from file or create default config"""
        default_config = {
            'window_size': '600x300',
            'bg_color': 'black',
            'fg_color': 'lime',
            'refresh_rate': 1000,
            'show_system_info': True,
            'minimize_to_tray': True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(loaded_config)
                    return default_config
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Refresh rate setting
        tk.Label(settings_window, text="Refresh Rate (ms):").pack(pady=5)
        refresh_var = tk.StringVar(value=str(self.refresh_rate))
        tk.Entry(settings_window, textvariable=refresh_var).pack(pady=5)
        
        # Color settings
        tk.Label(settings_window, text="Background Color:").pack(pady=5)
        bg_var = tk.StringVar(value=self.config.get('bg_color', 'black'))
        tk.Entry(settings_window, textvariable=bg_var).pack(pady=5)
        
        tk.Label(settings_window, text="Text Color:").pack(pady=5)
        fg_var = tk.StringVar(value=self.config.get('fg_color', 'lime'))
        tk.Entry(settings_window, textvariable=fg_var).pack(pady=5)
        
        def save_settings():
            try:
                self.refresh_rate = int(refresh_var.get())
                self.config['refresh_rate'] = self.refresh_rate
                self.config['bg_color'] = bg_var.get()
                self.config['fg_color'] = fg_var.get()
                
                # Apply colors immediately
                self.root.configure(bg=self.config['bg_color'])
                self.lbl.configure(bg=self.config['bg_color'], fg=self.config['fg_color'])
                
                self.save_config()
                settings_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Refresh rate must be a number!")
        
        tk.Button(settings_window, text="Save", command=save_settings).pack(pady=20)

    def minimize_to_tray(self):
        """Minimize application to system tray"""
        if not TRAY_AVAILABLE:
            messagebox.showinfo("Info", "System tray support not available. Install pystray and pillow.")
            return
            
        self.is_minimized_to_tray = True
        self.root.withdraw()
        
        # Create tray icon
        image = self.create_tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_from_tray),
            pystray.MenuItem("Exit", self.quit_from_tray)
        )
        
        self.tray_icon = pystray.Icon("PC Monitor", image, "PC Monitor", menu)
        
        # Run tray icon in separate thread
        def run_tray():
            self.tray_icon.run()
        
        threading.Thread(target=run_tray, daemon=True).start()

    def create_tray_image(self):
        """Create a simple tray icon image"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), 'black')
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, width, height), fill='black')
        dc.text((10, 20), "PC", fill='lime')
        return image

    def show_from_tray(self, icon=None, item=None):
        """Restore window from tray"""
        self.is_minimized_to_tray = False
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.root.deiconify()

    def quit_from_tray(self, icon=None, item=None):
        """Quit application from tray"""
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    def toggle_system_info(self):
        """Toggle system information display"""
        self.config['show_system_info'] = not self.config.get('show_system_info', True)
        self.save_config()

    def reset_window_size(self):
        """Reset window to default size"""
        self.root.geometry('600x300')

    def show_about(self):
        """Show about dialog"""
        about_text = f"""PC Monitor v1.1

A simple desktop application for monitoring
CPU and RAM usage in real time.

Features:
• Real-time system monitoring
• System tray support
• Customizable colors and refresh rate
• Responsive UI design

Platform: {platform.system()} {platform.release()}
Python: {platform.python_version()}

Created with Python, Tkinter, and psutil"""
        
        messagebox.showinfo("About PC Monitor", about_text)

    def show_system_info(self):
        """Show detailed system information"""
        try:
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info_text = f"""System Information:

🖥️ CPU Cores: {cpu_count}
⚡ CPU Frequency: {cpu_freq.current:.0f}MHz (Max: {cpu_freq.max:.0f}MHz)

💾 Total Memory: {memory.total // (1024**3):.1f}GB
📊 Available: {memory.available // (1024**3):.1f}GB
📈 Used: {memory.percent:.1f}%

💽 Disk Usage:
Total: {disk.total // (1024**3):.1f}GB
Used: {disk.used // (1024**3):.1f}GB ({disk.percent:.1f}%)
Free: {disk.free // (1024**3):.1f}GB"""
            
            messagebox.showinfo("System Information", info_text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve system info: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        if self.is_minimized_to_tray:
            self.show_from_tray()
        else:
            if messagebox.askokcancel("Quit", "Do you want to quit PC Monitor?"):
                if self.tray_icon:
                    self.tray_icon.stop()
                self.root.quit()

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Application error: {str(e)}")
            if self.tray_icon:
                self.tray_icon.stop()
            raise

# Minimize to tray feature (platform-dependent, requires extra packages like pystray)
# For now, we leave a placeholder for future implementation.

if __name__ == "__main__":
    app = PCMonitorApp()
    app.run()

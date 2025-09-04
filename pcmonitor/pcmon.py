
try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter is not installed.")
    exit(1)
try:
    import psutil
except ImportError:
    print("Error: psutil is not installed. Run 'pip install psutil'.")
    exit(1)

class PCMonitorApp:
    def __init__(self, refresh_rate=1000):
        self.root = tk.Tk()
        self.root.title("💻 CPU & RAM Monitor")
        self.root.geometry("600x300")
        self.root.configure(bg="black")
        self.root.minsize(300, 150)
        self.root.bind('<Configure>', self.on_resize)

        self.lbl = tk.Label(self.root, font=("Arial",30,"bold"), bg="black", fg="lime")
        self.lbl.pack(expand=True, fill='both')

        self.exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 14), bg="red", fg="white")
        self.exit_btn.pack(side="bottom", pady=10)

        self.refresh_rate = refresh_rate
        self.update()

    def update(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.lbl.config(text=f"💻 CPU Usage: {cpu}%\n💾 RAM Usage: {ram}%")
        except Exception as e:
            self.lbl.config(text=f"Error: {e}")
        self.root.after(self.refresh_rate, self.update)

    def on_resize(self, event):
        # Responsive font size based on window height
        new_size = max(12, int(event.height / 10))
        self.lbl.config(font=("Arial", new_size, "bold"))

    def run(self):
        self.root.mainloop()

# Minimize to tray feature (platform-dependent, requires extra packages like pystray)
# For now, we leave a placeholder for future implementation.

if __name__ == "__main__":
    app = PCMonitorApp()
    app.run()
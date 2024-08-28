# splash_screen.py
import tkinter as tk
import time

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.geometry("400x300")
        self.overrideredirect(True)  # Removes window decorations (title bar, etc.)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Add a splash image or text
        splash_label = tk.Label(self, text="Journal App", font=("Helvetica", 24))
        splash_label.pack(expand=True)
        
        # Optionally add a loading animation or progress bar here

    def show(self, duration=3000):
        """Show the splash screen for a given duration (in milliseconds)."""
        self.after(duration, self.destroy)  # Automatically close after duration
        self.mainloop()


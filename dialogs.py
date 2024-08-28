# dialogs.py
import tkinter as tk
from tkinter import simpledialog, colorchooser

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Settings")
        self.geometry("400x300")
        
        # Example: Theme selection option
        self.theme_label = tk.Label(self, text="Select Theme:")
        self.theme_label.pack(pady=10)

        self.theme_var = tk.StringVar(value="light")
        self.light_theme_radio = tk.Radiobutton(self, text="Light", variable=self.theme_var, value="light")
        self.dark_theme_radio = tk.Radiobutton(self, text="Dark", variable=self.theme_var, value="dark")

        self.light_theme_radio.pack(anchor=tk.W)
        self.dark_theme_radio.pack(anchor=tk.W)

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.save_settings)
        self.save_button.pack(pady=20)

    def show(self):
        self.grab_set()
        self.wait_window()

    def save_settings(self):
        selected_theme = self.theme_var.get()
        # Apply theme based on selection
        self.master.apply_theme(selected_theme)
        self.destroy()

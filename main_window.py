# main_window.py
import tkinter as tk
from ui.splash_screen import SplashScreen
from ui.widgets import CalendarWidget, TextEditor
from ui.dialogs import SettingsDialog
from ui.themes import apply_theme

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Journal App")
        self.geometry("800x600")
        
        # Apply the default theme
        apply_theme(self, "light")

        # Create and pack the main widgets
        self.create_widgets()

    def create_widgets(self):
        # Calendar Widget
        self.calendar = CalendarWidget(self)
        self.calendar.pack(side=tk.LEFT, fill=tk.Y)

        # Text Editor Widget
        self.text_editor = TextEditor(self)
        self.text_editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Menu Bar
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Entry", command=self.new_entry)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def new_entry(self):
        self.text_editor.clear()

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.show()

if __name__ == "__main__":
    # Show the splash screen before launching the main window
    root = MainWindow()
    splash = SplashScreen(root)
    splash.show(duration=3000)  # Show splash for 3 seconds

    root.deiconify()  # Show the main window after the splash screen
    root.mainloop()

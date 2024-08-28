# main_window.py
import tkinter as tk
from ui.splash_screen import SplashScreen

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially

    # Show the splash screen
    splash = SplashScreen(root)
    splash.show(duration=3000)  # Show splash for 3 seconds

    root.deiconify()  # Show the main window after the splash screen
    root.mainloop()

if __name__ == "__main__":
    main()
                              
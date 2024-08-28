# widgets.py
import tkinter as tk
from tkinter import scrolledtext
import tkcalendar as tkc  # Assuming you're using tkcalendar for the calendar widget

class CalendarWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add Calendar widget
        self.calendar = tkc.Calendar(self, selectmode="day")
        self.calendar.pack(fill=tk.BOTH, expand=True)

class TextEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Add ScrolledText widget for text editing
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def clear(self):
        self.text_area.delete(1.0, tk.END)

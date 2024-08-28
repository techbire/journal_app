# themes.py
def apply_theme(widget, theme):
    if theme == "light":
        widget.config(bg="white", fg="black")
    elif theme == "dark":
        widget.config(bg="black", fg="white")

    for child in widget.winfo_children():
        apply_theme(child, theme)

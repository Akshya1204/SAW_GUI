"""Reusable WindowUtilsMixin UI/application mixin."""

import tkinter as tk

class WindowUtilsMixin:
    def center_window(self, window: tk.Misc) -> None:
        window.update_idletasks()

        width = window.winfo_width()
        height = window.winfo_height()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x}+{y}")


"""Reusable mouse-wheel bindings for Tkinter scrollable regions."""

import tkinter as tk
from tkinter import ttk
from typing import Callable


ScrollCommand = Callable[[int, str], object]


def bind_mousewheel(widget: tk.Misc, scroll_command: ScrollCommand) -> None:
    """Bind vertical wheel scrolling to a widget and its child controls."""

    def on_mousewheel(event):
        delta = getattr(event, "delta", 0)
        if delta:
            amount = max(1, abs(delta) // 120)
            units = -amount if delta > 0 else amount
        else:
            units = -1 if getattr(event, "num", 5) == 4 else 1
        scroll_command(units, "units")
        return "break"

    def bind_children(parent: tk.Misc) -> None:
        if not isinstance(parent, ttk.Combobox):
            parent.bind("<MouseWheel>", on_mousewheel)
            parent.bind("<Button-4>", on_mousewheel)
            parent.bind("<Button-5>", on_mousewheel)

        for child in parent.winfo_children():
            bind_children(child)

    bind_children(widget)

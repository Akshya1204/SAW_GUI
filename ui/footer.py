"""Reusable FooterMixin UI/application mixin."""

import tkinter as tk
from utils.constants import *

class FooterMixin:
    root: tk.Tk

    def create_footer(self):
        footer = tk.Frame(self.root, bg=WHITE, height=32)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Frame(
            footer, bg=BORDER, height=1
        ).pack(fill="x")

        tk.Label(
            footer,
            text="● System Ready",
            font=(FONT_FAMILY, 8),
            fg=SUCCESS,
            bg=WHITE,
        ).pack(side="left", padx=20)

        tk.Label(
            footer,
            text="Specimen Analysis Workflow",
            font=(FONT_FAMILY, 8),
            fg=MUTED_TEXT,
            bg=WHITE,
        ).pack(side="right", padx=20)


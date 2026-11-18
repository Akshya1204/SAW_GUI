"""Instructions page for the application menu."""

import tkinter as tk

from utils.constants import *


class InstructionsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BACKGROUND)
        self.app = app
        self.build()


    def build(self):

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=24, pady=22)
        card = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=WHITE)
        inner.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            inner,
            text="SAW Workflow Instructions",
            font=(FONT_FAMILY, 20, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            justify="center",
        ).pack(fill="x")
        tk.Label(
            inner,
            text="A quick guide to preparing and reviewing a specimen analysis.",
            font=(FONT_FAMILY, 9),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
            justify="center",
        ).pack(fill="x", pady=(5, 18))

        paragraphs = [
            (
                "SAW organizes specimen, template, material, crack, and "
                "interpolation information into separate workflow sections. "
                "Each section can contain one or more records."
            ),
            (
                "Use the navigation bar to move between sections. The main "
                "table is read-only for review, while Add New and Update "
                "Existing open an Excel-style grid for data entry."
            ),
            (
                "Complete all workflow sections before starting analysis. "
                "The Home page shows the current completion state and keeps "
                "analysis unavailable until every section has data."
            ),
        ]
        for paragraph in paragraphs:
            tk.Label(
                inner,
                text=paragraph,
                font=(FONT_FAMILY, 10),
                fg=TEXT,
                bg=WHITE,
                justify="left",
                anchor="w",
                wraplength=680,
            ).pack(fill="x", anchor="w", pady=(0, 12))

        tk.Label(
            inner,
            text="Recommended workflow",
            font=(FONT_FAMILY, 12, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            justify="center",
        ).pack(fill="x", pady=(5, 8))

        bullet_points = [
            "Start with Specimen Definition and identify the specimen clearly.",
            "Add the template and finite-element material information.",
            "Complete crack propagation and crack geometry details.",
            "Add interpolation file information when external data is required.",
            "Review each table, then use Submit before running the analysis.",
        ]
        bullets = tk.Frame(inner, bg=WHITE)
        bullets.pack(fill="x", anchor="w")
        for point in bullet_points:
            row = tk.Frame(bullets, bg=WHITE)
            row.pack(fill="x", pady=3)
            tk.Label(
                row,
                text="•",
                font=(FONT_FAMILY, 11, "bold"),
                fg=EDIT_FOCUS,
                bg=WHITE,
                width=3,
                anchor="w",
            ).pack(side="left")
            tk.Label(
                row,
                text=point,
                font=(FONT_FAMILY, 9),
                fg=TEXT,
                bg=WHITE,
                justify="left",
                anchor="w",
                wraplength=650,
            ).pack(side="left", fill="x", expand=True)

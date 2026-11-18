"""Reusable MainUIMixin UI/application mixin."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, Dict

from utils.constants import *


class MainUIMixin:
    root: tk.Tk
    header: tk.Frame
    content: tk.Frame
    menu_button: tk.Button
    child_windows: Dict[str, tk.Toplevel]

    if TYPE_CHECKING:
        def toggle_menu(self) -> None:
            ...

    def create_header(self):
        self.header = tk.Frame(self.root, bg=DARK_HEADER, height=72)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        icon_frame = tk.Frame(
            self.header, bg=PRIMARY, width=42, height=42
        )
        icon_frame.pack(side="left", padx=(20, 12), pady=15)
        icon_frame.pack_propagate(False)

        tk.Label(
            icon_frame,
            text="SA",
            font=(FONT_FAMILY, 12, "bold"),
            fg=WHITE,
            bg=PRIMARY,
        ).pack(expand=True)

        title_container = tk.Frame(self.header, bg=DARK_HEADER)
        title_container.pack(side="left", fill="y")

        tk.Label(
            title_container,
            text=APP_TITLE,
            font=(FONT_FAMILY, 15, "bold"),
            fg=WHITE,
            bg=DARK_HEADER,
        ).pack(anchor="w", pady=(13, 0))

        tk.Label(
            title_container,
            text="Engineering Material Analysis Platform",
            font=(FONT_FAMILY, 8),
            fg=HEADER_MUTED,
            bg=DARK_HEADER,
        ).pack(anchor="w")

        version_frame = tk.Frame(self.header, bg=DARK_HEADER)
        version_frame.pack(side="right", padx=(10, 15))

        tk.Label(
            version_frame,
            text=f"v{APP_VERSION}",
            font=(FONT_FAMILY, 9, "bold"),
            fg=HEADER_VERSION,
            bg=DARK_HEADER,
        ).pack()

        self.menu_button = tk.Button(
            self.header,
            text="⋮",
            font=(FONT_FAMILY, 20, "bold"),
            fg=WHITE,
            bg=DARK_HEADER,
            activebackground=DARK_HEADER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_menu,
        )
        self.menu_button.pack(side="right", padx=(5, 8))


    def create_dashboard(self):
        main_area = tk.Frame(self.root, bg=BACKGROUND)
        main_area.pack(fill="both", expand=True)

        self.content = tk.Frame(main_area, bg=BACKGROUND)
        self.content.pack(fill="both", expand=True, padx=20, pady=18)


    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


    def create_status_card(
        self, parent, title, value, accent, light_background
    ):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

        body = tk.Frame(card, bg=WHITE)
        body.pack(fill="both", expand=True, padx=15, pady=12)

        tk.Label(
            body,
            text=title,
            font=(FONT_FAMILY, 8),
            fg=SECONDARY_TEXT,
            bg=WHITE,
        ).pack(anchor="w")

        tk.Label(
            body,
            text=value,
            font=(FONT_FAMILY, 13, "bold"),
            fg=accent,
            bg=WHITE,
        ).pack(anchor="w", pady=(4, 0))


    def create_dashboard_home(self):
        self.clear_content()

        welcome = tk.Frame(self.content, bg=BACKGROUND)
        welcome.pack(fill="x")

        tk.Label(
            welcome,
            text="Welcome to SAW",
            font=(FONT_FAMILY, 24, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text=(
                "Manage specimen definitions, materials, templates "
                "and analysis configuration from one workspace."
            ),
            font=(FONT_FAMILY, 10),
            fg=SECONDARY_TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(5, 0))

        cards_container = tk.Frame(self.content, bg=BACKGROUND)
        cards_container.pack(fill="x", pady=(30, 25))

        self.create_status_card(
            cards_container, "Application Status", "Ready",
            SUCCESS, SUCCESS_LIGHT
        )
        self.create_status_card(
            cards_container, "Available Modules",
            str(len(NAVIGATION_OPTIONS)), PRIMARY, PRIMARY_LIGHT
        )
        self.create_status_card(
            cards_container, "Workflow", "Ready to Start",
            SECONDARY_ACCENT, SECONDARY_ACCENT_LIGHT
        )

        workspace = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        workspace.pack(fill="both", expand=True)

        tk.Label(
            workspace,
            text="Workspace",
            font=(FONT_FAMILY, 13, "bold"),
            fg=TEXT,
            bg=WHITE,
        ).pack(anchor="w", padx=20, pady=16)

        tk.Frame(workspace, bg=BORDER, height=1).pack(fill="x")

        body = tk.Frame(workspace, bg=WHITE)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text="＋",
            font=(FONT_FAMILY, 30),
            fg=PRIMARY,
            bg=WHITE,
        ).pack(pady=(35, 5))

        tk.Label(
            body,
            text="Select a module to begin",
            font=(FONT_FAMILY, 13, "bold"),
            fg=TEXT,
            bg=WHITE,
        ).pack()

        tk.Label(
            body,
            text="Choose a navigation option above to open its workspace.",
            font=(FONT_FAMILY, 9),
            fg=SECONDARY_TEXT,
            bg=WHITE,
        ).pack(pady=(5, 20))


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


    def center_window(self, window):
        window.update_idletasks()

        width = window.winfo_width()
        height = window.winfo_height()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x}+{y}")


    def close_child_window(self, option):
        if option in self.child_windows:
            window = self.child_windows[option]

            if window.winfo_exists():
                window.destroy()

            del self.child_windows[option]


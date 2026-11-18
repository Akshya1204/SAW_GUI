"""Application menu and secondary page windows."""

import tkinter as tk
from typing import TYPE_CHECKING, Dict, Optional

from ui.pages.instructions_page import InstructionsPage
from ui.pages.settings_page import CombinedSettingsPage
from utils.constants import *


class MenuMixin:
    root: tk.Tk
    menu_frame: Optional[tk.Frame]
    child_windows: Dict[str, tk.Toplevel]

    if TYPE_CHECKING:
        def close_application(self) -> None:
            ...

        def close_child_window(self, option: str) -> None:
            ...

        def center_window(self, window: tk.Misc) -> None:
            ...

    def toggle_menu(self):
        if self.menu_frame is not None:
            self.close_menu()
        else:
            self.open_menu()


    def open_menu(self):
        self.menu_frame = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.root.update_idletasks()
        x = max(self.root.winfo_width() - 235, 0)
        y = 65
        self.menu_frame.place(x=x, y=y, width=220)

        for icon, option in HAMBURGER_OPTIONS:
            self.create_menu_item(icon, option)


    def create_menu_item(self, icon, option):
        item = tk.Frame(self.menu_frame, bg=WHITE, cursor="hand2")
        item.pack(fill="x")

        icon_label = tk.Label(
            item,
            text=icon,
            font=(FONT_FAMILY, 11),
            fg=TEXT,
            bg=WHITE,
            width=3,
        )
        icon_label.pack(side="left", padx=(8, 0), pady=9)

        text_label = tk.Label(
            item,
            text=option,
            font=(FONT_FAMILY, 10),
            fg=TEXT,
            bg=WHITE,
            anchor="w",
        )
        text_label.pack(side="left", fill="x", expand=True, padx=5, pady=9)

        for widget in (item, icon_label, text_label):
            widget.bind(
                "<Button-1>",
                lambda event, name=option: self.open_menu_window(name),
            )
            widget.bind(
                "<Enter>",
                lambda event, frame=item: self.menu_hover(frame, True),
            )
            widget.bind(
                "<Leave>",
                lambda event, frame=item: self.menu_hover(frame, False),
            )


    def menu_hover(self, item, is_hover):
        background = HOVER_BG if is_hover else WHITE
        item.configure(bg=background)
        for child in item.winfo_children():
            child.configure(bg=background)


    def open_menu_window(self, option, initial_tab="settings"):
        self.close_menu()

        if option == "Exit":
            self.close_application()
            return

        if option in self.child_windows:
            existing = self.child_windows[option]
            if existing.winfo_exists():
                existing.lift()
                existing.focus_force()
                if option == "Settings" and hasattr(existing, "saw_settings_page"):
                    existing.saw_settings_page.select_tab(initial_tab)
                return

        window = tk.Toplevel(self.root)
        self.child_windows[option] = window
        window.title(f"{option} - {APP_SHORT_NAME}")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if option == "Settings":
            window_width = min(920, max(700, screen_width - 80))
            window_height = min(760, max(600, screen_height - 120))
            page_class = CombinedSettingsPage
        else:
            window_width = min(780, max(620, screen_width - 80))
            window_height = min(640, max(500, screen_height - 120))
            page_class = InstructionsPage

        window.geometry(f"{window_width}x{window_height}")
        window.minsize(
            min(620, window_width),
            min(500, window_height),
        )
        window.configure(bg=BACKGROUND)
        window.resizable(True, True)
        window.overrideredirect(False)
        try:
            window.wm_attributes("-toolwindow", False)
        except tk.TclError:
            pass
        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_child_window(option),
        )
        self.center_window(window)

        if option == "Settings":
            page = page_class(window, self, initial_tab=initial_tab)
            window.saw_settings_page = page
        else:
            page = page_class(window, self)
        page.pack(fill="both", expand=True)


    def close_menu(self):
        if self.menu_frame is not None:
            self.menu_frame.destroy()
            self.menu_frame = None

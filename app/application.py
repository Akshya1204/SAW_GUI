"""SAW application composition and startup lifecycle."""

import tkinter as tk
from typing import Dict, List, Optional

from utils.constants import *
from ui.main_ui import MainUIMixin
from ui.navigation import NavigationMixin
from ui.menu import MenuMixin
from app.lifecycle import LifecycleMixin


class SAWApplication(
    MainUIMixin,
    NavigationMixin,
    MenuMixin,
    LifecycleMixin,
):
    root: tk.Tk
    header: tk.Frame
    navigation: tk.Frame
    content: tk.Frame
    navigation_buttons: Dict[str, tk.Button]
    current_module: Optional[str]
    current_page: Optional[tk.Frame]
    configuration_statuses: Dict[str, Dict[str, str]]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.child_windows: Dict[str, tk.Toplevel] = {}
        self.menu_frame: Optional[tk.Frame] = None
        self.navigation_buttons = {}

        # Each module keeps its own in-memory table data.
        self.module_data: Dict[str, List[List[str]]] = {
            name: [] for name in NAVIGATION_OPTIONS
        }
        self.module_completion: Dict[str, bool] = {
            name: False for name in NAVIGATION_OPTIONS if name != "Home"
        }
        
        # Track workflow sections explicitly skipped by the user
        self.module_skipped: Dict[str, bool] = {
            name: False
            for name in NAVIGATION_OPTIONS
            if name != "Home"
        }

        self.current_module = None
        self.current_page = None
        self.settings_values: Dict[str, str] = {}
        self.configuration_statuses: Dict[str, Dict[str, str]] = {}

        self.configure_root()
        self.create_header()
        self.create_navigation()
        self.create_dashboard()
        self.create_footer()

        # Home is the default landing page.
        self.show_home()


    def configure_root(self):
        self.root.title(f"{APP_TITLE} - {APP_SHORT_NAME}")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        available_width = max(700, screen_width - 80)
        available_height = max(450, screen_height - 120)
        window_width = min(WINDOW_WIDTH, available_width)
        window_height = min(WINDOW_HEIGHT, available_height)

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(
            min(MIN_WIDTH, available_width),
            min(MIN_HEIGHT, available_height),
        )
        self.root.configure(bg=BACKGROUND)
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)


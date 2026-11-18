"""Application navigation and page routing."""

import tkinter as tk
from typing import Dict, Optional, Protocol

from ui.pages.home_page import HomePage
from ui.pages.registry import PAGE_REGISTRY
from utils.constants import *


class NavigationHost(Protocol):
    """Runtime host contract supplied by the composed application class."""

    root: tk.Tk
    navigation: tk.Frame
    navigation_buttons: Dict[str, tk.Button]
    content: tk.Frame
    current_module: Optional[str]
    current_page: Optional[tk.Frame]

    def clear_content(self) -> None:
        ...

    def navigation_hover(self, button: tk.Button, is_hover: bool) -> None:
        ...

    def set_active_navigation(self, selected_option: str) -> None:
        ...

    def show_home(self) -> None:
        ...

    def show_module(self, module_name: str) -> None:
        ...


class NavigationMixin:
    def create_navigation(self: NavigationHost) -> None:
        self.navigation = tk.Frame(self.root, bg=WHITE, height=76)
        self.navigation.pack(fill="x")
        self.navigation.pack_propagate(False)

        tk.Frame(
            self.navigation, bg=BORDER, height=1
        ).pack(side="bottom", fill="x")

        navigation_container = tk.Frame(self.navigation, bg=WHITE)
        navigation_container.pack(fill="both", expand=True, padx=8)
        navigation_container.grid_rowconfigure(0, weight=1)

        for index, option in enumerate(NAVIGATION_OPTIONS):
            navigation_container.grid_columnconfigure(
                index, weight=1, uniform="navigation"
            )

            button = tk.Button(
                navigation_container,
                text=option,
                font=(FONT_FAMILY, 8, "bold"),
                fg=TEXT,
                bg=WHITE,
                activeforeground=PRIMARY,
                activebackground=NAV_ACTIVE,
                relief="flat",
                bd=0,
                padx=4,
                pady=4,
                wraplength=105,
                justify="center",
                cursor="hand2",
                command=lambda name=option: self.show_module(name),
            )
            button.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=2,
                pady=8,
            )
            self.navigation_buttons[option] = button
            button.bind(
                "<Enter>",
                lambda event, btn=button: self.navigation_hover(btn, True),
            )
            button.bind(
                "<Leave>",
                lambda event, btn=button: self.navigation_hover(btn, False),
            )


    def navigation_hover(
        self: NavigationHost,
        button: tk.Button,
        is_hover: bool,
    ) -> None:
        if button.cget("fg") == PRIMARY:
            return
        button.configure(bg=HOVER_BG if is_hover else WHITE)


    def show_home(self: NavigationHost) -> None:
        self.current_module = "Home"
        self.set_active_navigation("Home")
        self.clear_content()
        page = HomePage(self.content, self)
        page.pack(fill="both", expand=True)
        self.current_page = page


    def show_module(self: NavigationHost, module_name: str) -> None:
        if module_name == "Home":
            self.show_home()
            return

        page_class = PAGE_REGISTRY.get(module_name)
        if page_class is None:
            return

        self.current_module = module_name
        self.set_active_navigation(module_name)
        self.clear_content()
        page = page_class(self.content, self)
        page.pack(fill="both", expand=True)
        self.current_page = page


    def set_active_navigation(
        self: NavigationHost,
        selected_option: str,
    ) -> None:
        for option, button in self.navigation_buttons.items():
            if option == selected_option:
                button.configure(bg=NAV_ACTIVE, fg=PRIMARY)
            else:
                button.configure(bg=WHITE, fg=TEXT)

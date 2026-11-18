"""Home workflow dashboard page."""

import tkinter as tk
from typing import Optional

from ui.dialogs.configuration_dialog import (
    CONFIGURATION_WINDOW_KEY,
    ConfigurationDialog,
)
from utils.constants import *


class HomePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=EDIT_SURFACE)
        self.app = app
        self.build()


    def build(self):
        hero = tk.Frame(
            self,
            bg=ENTERPRISE_BLUE,
            padx=22,
            pady=16,
        )
        hero.pack(fill="x", padx=22, pady=(12, 10))

        tk.Label(
            hero,
            text="Specimen Analysis Workflow",
            font=(FONT_FAMILY, 22, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
            justify="center",
        ).pack(fill="x")

        tk.Label(
            hero,
            text="Welcome to SAW",
            font=(FONT_FAMILY, 10),
            fg=HEADER_MUTED,
            bg=ENTERPRISE_BLUE,
            justify="center",
        ).pack(fill="x", pady=(7, 0))

        self.create_quick_actions()
        
        workflow_modules = [
            option for option in NAVIGATION_OPTIONS
            if option != "Home"
        ]
        completed_modules = [
            module for module in workflow_modules
            if self.is_section_complete(module)
            and not self.app.module_skipped.get(module, False)
        ]
        skipped_modules = [
            module for module in workflow_modules
            if self.app.module_skipped.get(module, False)
        ]
        resolved_modules = [
            module for module in workflow_modules
            if (
                self.is_section_complete(module)
                or self.app.module_skipped.get(module, False)
            )
        ]
        completed_count = len(completed_modules)
        skipped_count = len(skipped_modules)
        resolved_count = len(resolved_modules)
        total_count = len(workflow_modules)
        
        # All sections must be completed or skipped.
        # At least one section must actually be completed.
        analysis_ready = (
            resolved_count == total_count
            and completed_count > 0
        )
        # progress_ratio = completed_count / total_count if total_count else 0
        progress_ratio = (
            resolved_count / total_count
            if total_count else 0
        )
        completion_color = SUCCESS if analysis_ready else STATUS_INCOMPLETE
        completion_bg = (
            SUCCESS_LIGHT
            if analysis_ready
            else STATUS_INCOMPLETE_LIGHT
        )

        stepper = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            padx=24,
            pady=22,
        )
        stepper.pack(fill="both", expand=True, padx=22, pady=(0, 18))

        heading = tk.Frame(stepper, bg=WHITE)
        heading.pack(fill="x")
        heading.grid_columnconfigure(0, weight=1)
        heading.grid_columnconfigure(2, weight=1)

        heading_text = tk.Frame(heading, bg=WHITE)
        heading_text.grid(row=0, column=1)

        tk.Label(
            heading_text,
            text="Workflow Status",
            font=(FONT_FAMILY, 13, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            justify="center",
        ).pack(anchor="center")

        tk.Label(
            heading,
            text=f"{resolved_count}/{total_count} Resolved",
            font=(FONT_FAMILY, 9, "bold"),
            fg=completion_color,
            bg=completion_bg,
            padx=12,
            pady=6,
        ).grid(row=0, column=2, sticky="e", padx=(12, 0))

        progress_track = tk.Frame(stepper, bg=PROGRESS_TRACK, height=8)
        progress_track.pack(fill="x", pady=(18, 18))
        progress_track.pack_propagate(False)

        if progress_ratio:
            tk.Frame(progress_track, bg=SUCCESS).place(
                relx=0,
                rely=0,
                relwidth=progress_ratio,
                relheight=1,
            )

        steps_area = tk.Frame(stepper, bg=WHITE)
        steps_area.pack(fill="both", expand=True)

        steps = tk.Frame(steps_area, bg=WHITE)
        steps.pack(fill="x", expand=True, anchor="center")

        for column_index in range((len(workflow_modules) * 2) - 1):
            weight = 1 if column_index % 2 == 0 else 0
            steps.grid_columnconfigure(column_index, weight=weight)

        for index, module_name in enumerate(workflow_modules):
            is_complete = self.is_section_complete(module_name)
            is_skipped = self.app.module_skipped.get(module_name, False)
            
            if is_skipped:
                status_text = "Skipped"
                color = ENTERPRISE_MUTED
                light_color = BACKGROUND
            elif is_complete:
                status_text = "Complete"
                color = SUCCESS
                light_color = SUCCESS_LIGHT
            else:
                status_text = "Pending"
                color = STATUS_INCOMPLETE
                light_color = STATUS_INCOMPLETE_LIGHT
            # color = SUCCESS if is_complete else STATUS_INCOMPLETE
            # light_color = (
            #     SUCCESS_LIGHT
            #     if is_complete
            #     else STATUS_INCOMPLETE_LIGHT
            # )
            # status_text = "Complete" if is_complete else "Pending"
            step_column = index * 2

            step = tk.Frame(steps, bg=WHITE, cursor="hand2")
            step.grid(row=0, column=step_column, sticky="n", padx=3)

            marker = tk.Label(
                step,
                text=f"{index + 1:02}",
                font=(FONT_FAMILY, 10, "bold"),
                fg=WHITE,
                bg=color,
                width=4,
                pady=5,
            )
            marker.pack()

            tk.Label(
                step,
                text=module_name,
                font=(FONT_FAMILY, 9, "bold"),
                fg=ENTERPRISE_TEXT,
                bg=WHITE,
                wraplength=135,
                justify="center",
            ).pack(pady=(8, 4))

            tk.Label(
                step,
                text=status_text,
                font=(FONT_FAMILY, 8, "bold"),
                fg=color,
                bg=light_color,
                padx=8,
                pady=3,
            ).pack()
            
            skip_var = tk.BooleanVar(
                value=self.app.module_skipped.get(module_name, False))
            
            skip_checkbox = tk.Checkbutton(
                step,
                text="Skip",
                variable=skip_var,
                font=(FONT_FAMILY, 8),
                bg=WHITE,
                activebackground=WHITE,
                fg=ENTERPRISE_TEXT,
                selectcolor=WHITE,
                command=lambda name=module_name, var=skip_var: (
                    self.set_module_skipped(name, var.get())
                ),
            )
            skip_checkbox.pack(pady=(6, 0))

            for widget in step.winfo_children() + [step]:
                # Do not navigate when clicking skip checkbox
                if widget is skip_checkbox:
                    continue
                
                # Open the corresponding module when clicked
                widget.bind(
                    "<Button-1>",
                    lambda event, name=module_name:
                    self.app.show_module(name),
                )

            if index < len(workflow_modules) - 1:
                next_complete = self.is_section_complete(
                    workflow_modules[index + 1]
                )
                connector_color = (
                    SUCCESS
                    # if is_complete and next_complete
                    if (
                        (is_complete or is_skipped)
                        and (
                            next_complete
                            or self.app.module_skipped.get(
                                workflow_modules[index + 1], False
                            )
                        )
                    )
                    else STATUS_INCOMPLETE
                )
                tk.Frame(
                    steps,
                    bg=connector_color,
                    height=3,
                    width=34,
                ).grid(
                    row=0,
                    column=step_column + 1,
                    sticky="ew",
                    pady=(15, 0),
                )

        action_panel = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            padx=18,
            pady=9,
        )
        action_panel.pack(fill="x", padx=22, pady=(0, 10))

        status_block = tk.Frame(action_panel, bg=WHITE)
        status_block.pack(side="left")

        tk.Label(
            status_block,
            text="Ready" if analysis_ready else "Blocked",
            font=(FONT_FAMILY, 10, "bold"),
            fg=completion_color,
            bg=WHITE,
        ).pack(side="left")

        tk.Button(
            action_panel,
            text="Run Analysis",
            font=(FONT_FAMILY, 9, "bold"),
            fg=WHITE,
            disabledforeground=WHITE,
            bg=ENTERPRISE_BLUE if analysis_ready else DISABLED_ACTION,
            activebackground=PRIMARY_HOVER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2" if analysis_ready else "arrow",
            state="normal" if analysis_ready else "disabled",
            command=self.app.run_analysis,
        ).pack(side="left", padx=(18, 0))

        tk.Label(
            status_block,
            text=(
                f" {completed_count} complete, "
                f"{skipped_count} skipped, "
                f"{total_count - resolved_count} pending"
            ),
            
            font=(FONT_FAMILY, 9),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
        ).pack(side="left")

        self.create_action_button(
            action_panel,
            "Collate Specimen Results",
            lambda: self.open_home_action_window("Collate Specimen Results"),
            compact=True,
            side="right",
            fill=None,
            expand=False,
        )


    def create_quick_actions(self):
        quick_actions = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            padx=18,
            pady=14,
        )
        quick_actions.pack(fill="x", padx=22, pady=(0, 14))

        # Section Heading
        heading = tk.Frame(quick_actions, bg=WHITE)
        heading.pack(fill="x", pady=(0, 8))

        tk.Label(
            heading,
            text="Configure SAW",
            font=(FONT_FAMILY, 12, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        ).pack(anchor="center")

        # Separator
        separator = tk.Frame(quick_actions, bg=BORDER, height=1)
        separator.pack(fill="x", pady=(0, 10))
        separator.pack_propagate(False)

        # Container for three buttons
        row = tk.Frame(quick_actions, bg=WHITE)
        row.pack(fill="x")
        
        # for column_index in range(4):
        for column_index in range(3):
            row.grid_columnconfigure(
                column_index,
                weight=1,
                uniform="quick-action",
            )
        row.grid_rowconfigure(0, weight=1)

        # Only the three required buttons
        quick_action_labels = [
            "Check Config",
            "Run Unit Tests",
            "Run System Tests",
        ]
        for column_index, label in enumerate(quick_action_labels):
            
            self.create_action_button(
                row,
                label,
                lambda name=label: self.open_home_action_window(name),
                compact=True,
                grid_options={
                    "row": 0,
                    "column": column_index,
                    "sticky": "ew",
                    "padx": 5,
                    "pady": 5,
                },
            )


        # label = f"SAW Configuration"
        # command = (
        #     self.open_configuration_dialog
        # )
        # self.create_action_button(
        #     row,
        #     label,
        #     command,
        #     compact=True,
        #     grid_options={
        #         "row": 0,
        #         "column": 0,
        #         "sticky": "ew",
        #         "padx": 5,
        #         "pady": 5,
        #     },
        # )
        
        label = f"Check Config"
        command = (
            lambda name=label: self.open_home_action_window(name)
        )
        self.create_action_button(
            row,
            label,
            command,
            compact=True,
            grid_options={
                "row": 0,
                "column": 0,
                "sticky": "ew",
                "padx": 5,
                "pady": 5,
            },
        )
        
        label = f"Run Unit Tests"
        command = (
            lambda name=label: self.open_home_action_window(name)
        )
        self.create_action_button(
            row,
            label,
            command,
            compact=True,
            grid_options={
                "row": 0,
                "column": 1,
                "sticky": "ew",
                "padx": 5,
                "pady": 5,
            },
        )
        
        label = f"Run System Tests"
        command = (
            lambda name=label: self.open_home_action_window(name)
        )
        self.create_action_button(
            row,
            label,
            command,
            compact=True,
            grid_options={
                "row": 0,
                "column": 2,
                "sticky": "ew",
                "padx": 5,
                "pady": 5,
            },
        )


    def open_configuration_dialog(self) -> None:
        """Open the Configuration tab in the shared Settings window."""
        self.app.open_menu_window("Settings", initial_tab="configuration")


    def create_action_button(
        self,
        parent,
        label,
        command,
        is_last=False,
        compact=False,
        side="left",
        fill: Optional[str] = "both",
        expand=True,
        grid_options: Optional[dict] = None,
    ):
        button = tk.Button(
            parent,
            text=label,
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            activeforeground=ENTERPRISE_BLUE,
            activebackground=ENTERPRISE_BLUE_LIGHT,
            relief="flat",
            bd=0,
            highlightbackground=ENTERPRISE_BORDER,
            highlightcolor=EDIT_FOCUS,
            highlightthickness=1,
            padx=8 if compact else 10,
            pady=12 if compact else 10,
            cursor="hand2",
            command=command,
        )
        if grid_options is not None:
            button.grid(**grid_options)
        else:
            pack_options = {
                "side": side,
                "expand": expand,
                "padx": (0, 8) if not is_last and side == "left" else (0, 0),
            }
            if fill:
                pack_options["fill"] = fill
            button.pack(**pack_options)
        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg=ENTERPRISE_BLUE_LIGHT,
                fg=ENTERPRISE_BLUE,
            ),
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=WHITE,
                fg=ENTERPRISE_TEXT,
            ),
        )
        
    def set_module_skipped(self, module_name, skipped):
        """Update the skip status and refresh Home."""
        self.app.module_skipped[module_name] = bool(skipped)
        
        # Refresh Home to update status, progress,
        # and Run Analysis button.
        self.app.show_home()

    def is_section_complete(self, module_name):
        return bool(self.app.module_completion.get(module_name, False))


    def open_home_action_window(self, button_name):
        window_key = f"home_action:{button_name}"
        existing = self.app.child_windows.get(window_key)
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_force()
            return

        window = tk.Toplevel(self.app.root)
        self.app.child_windows[window_key] = window
        window.title(f"{button_name} - {APP_SHORT_NAME}")
        window.geometry("540x340")
        window.minsize(460, 300)
        window.configure(bg=BACKGROUND)
        window.resizable(True, True)
        window.overrideredirect(False)
        try:
            window.wm_attributes("-toolwindow", False)
        except tk.TclError:
            pass
        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.app.close_child_window(window_key),
        )
        self.app.center_window(window)

        header = tk.Frame(window, bg=ENTERPRISE_BLUE, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text=button_name,
            font=(FONT_FAMILY, 14, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
        ).pack(side="left", padx=20)

        content = tk.Frame(
            window,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        content.pack(fill="both", expand=True, padx=24, pady=24)
        tk.Label(
            content,
            text=f"{button_name} window",
            font=(FONT_FAMILY, 18, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        ).pack(pady=(55, 8))
        tk.Label(
            content,
            text="This action is ready for its future functionality.",
            font=(FONT_FAMILY, 9),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
        ).pack()
        tk.Button(
            content,
            text="Close",
            font=(FONT_FAMILY, 9, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
            activebackground=PRIMARY_HOVER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda: self.app.close_child_window(window_key),
        ).pack(pady=(24, 0))

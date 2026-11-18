"""Reusable LifecycleMixin UI/application mixin."""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Optional, TYPE_CHECKING

from utils.constants import NAVIGATION_OPTIONS


class LifecycleMixin:
    root: tk.Tk
    current_module: Optional[str]
    module_data: Dict[str, List[List[str]]]
    module_completion: Dict[str, bool]
    child_windows: Dict[str, tk.Toplevel]

    if TYPE_CHECKING:
        def close_menu(self) -> None:
            ...

    def submit_data(self):
        if not self.current_module:
            return

        self.submit_data_for_module(self.current_module)


    def submit_data_for_module(self, module_name):
        rows = self.module_data.get(module_name, [])

        if not rows:
            messagebox.showwarning(
                "No Data",
                "There is no data to submit.",
                parent=self.root,
            )
            return False

        self.module_completion[module_name] = True

        messagebox.showinfo(
            "Submitted",
            f"{len(rows)} row(s) submitted for "
            f"{module_name}.",
            parent=self.root,
        )
        return True


    def mark_module_incomplete(self, module_name):
        if module_name in self.module_completion:
            self.module_completion[module_name] = False


    def run_analysis(self):
        workflow_modules = [
            option for option in NAVIGATION_OPTIONS 
            if option != "Home"
        ]
        incomplete_modules = [
            module for module in workflow_modules
            # if not self.module_completion.get(module, False)
            if not (
                self.module_completion.get(module, False)
                or self.module_skipped.get(module, False)
            )
        ]

        if incomplete_modules:
            messagebox.showwarning(
                "Analysis Blocked",
                "Please complete or skip the following "
                "workflow sections:\n\n"
                + "\n".join(incomplete_modules),
                parent=self.root,
            )
            return
        
        active_modules = [
            module for module in workflow_modules
            if not self.module_skipped.get(module, False)
        ]
        
        if not any(
            self.module_completion.get(module, False)
            for module in active_modules
        ):
            messagebox.showwarning(
                "Analysis Blocked",
                "At least one workflow section must be "
                "completed before running analysis.",
                parent=self.root,
            )
            return
        
        skipped_modules = [
            module for module in workflow_modules
            if self.module_skipped.get(module, False)
        ]

        messagebox.showinfo(
            "Run Analysis",
            "All workflow workflow sections are resolved.\n\n"
            f"Completed: {len(active_modules)}\n"
            f"Skipped: {len(skipped_modules)}\n\n"
            "The workflow readiness check has passed.",
            parent=self.root,
        )


    def close_application(self):
        self.close_menu()

        for window in list(self.child_windows.values()):
            try:
                if window.winfo_exists():
                    window.destroy()
            except tk.TclError:
                pass

        self.root.destroy()


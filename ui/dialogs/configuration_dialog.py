"""Modal SAW tool configuration dialog opened from Home Button 2."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, Optional, Tuple

from ui.widgets.mousewheel import bind_mousewheel
from utils.constants import *
from validation.mandatory_fields import create_field_label


CONFIGURATION_WINDOW_KEY = "home_action:Button 2"

CONFIGURATION_FIELDS: Tuple[Dict[str, str], ...] = (
    {
        "label": "Darwin Folder",
        "key": "darwin_folder",
        "control_type": "folder",
        "action": "check",
        "required": True,
    },
    {
        "label": "Darwin License Key",
        "key": "darwin_key",
        "control_type": "text",
        "action": "validate",
        "required": True,
    },
    {
        "label": "Darwin Executable Path",
        "key": "darwin_path",
        "control_type": "file",
        "action": "check",
        "required": True,
    },
    # {
    #     "label": "Folder Containing run_saw.py",
    #     "key": "folder_containing_run_saw",
    #     "control_type": "folder",
    #     "action": "check",
    #     "required": True,
    # },
    # {
    #     "label": "Path to Python Executable",
    #     "key": "path_to_python_executable",
    #     "control_type": "file",
    #     "action": "check",
    #     "required": True,
    # },
    {
        "label": "SC03 Path",
        "key": "sc03_path",
        "control_type": "file",
        "action": "check",
        "required": True,
    },
    {
        "label": "SK13 Path",
        "key": "sk13_path",
        "control_type": "file",
        "action": "check",
        "required": True,
    },
    {
        "label": "SK13 Generator",
        "key": "sk13_gen",
        "control_type": "file",
        "action": "check",
        "required": True,
    },
    {
        "label": "SK19 Folder",
        "key": "sk19_folder",
        "control_type": "folder",
        "action": "check",
        "required": True,
    },
    {
        "label": "SK19 Generator",
        "key": "sk19_gen",
        "control_type": "file",
        "action": "check",
        "required": True,
    },
)

STATUS_TEXT = "Not checked"
STATUS_NEUTRAL = "neutral"
STATUS_SUCCESS = "success"
STATUS_WARNING = "warning"
STATUS_ERROR = "error"


class ConfigurationDialog:
    """Responsive, modal configuration editor for SAW tool paths."""

    def __init__(self, parent: tk.Misc, app: Any, embedded_parent=None):
        self.parent = parent
        self.app = app
        self.window_key = CONFIGURATION_WINDOW_KEY
        self.entries: Dict[str, tk.Entry] = {}
        self.status_labels: Dict[str, tk.Label] = {}
        self.status_values: Dict[str, Dict[str, str]] = {}
        self.closed = False

        self.embedded = embedded_parent is not None
        if self.embedded:
            # Build the existing form inside the Settings notebook tab.
            self.window = embedded_parent.winfo_toplevel()
            self.host = tk.Frame(embedded_parent, bg=BACKGROUND)
            self.host.pack(fill="both", expand=True)
        else:
            self.window = tk.Toplevel(parent)
            self.host = self.window
            self.window.title("SAW Tool Configuration")
            self.window.configure(bg=BACKGROUND)
            self.window.resizable(True, True)
            self.window.overrideredirect(False)
            try:
                self.window.wm_attributes("-toolwindow", False)
            except tk.TclError:
                pass
            self.window.minsize(760, 520)
            self.window.protocol("WM_DELETE_WINDOW", self.close)
            self.window.bind("<Escape>", self._close_from_event)
            self.window.bind("<Return>", self._save_from_event)

        self.build()
        if not self.embedded:
            self.center_window(parent)
            self.window.grab_set()
            self.window.focus_force()

    def build(self) -> None:
        info = tk.Frame(
            self.host,
            bg=ENTERPRISE_BLUE_LIGHT,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        info.pack(fill="x", padx=18, pady=(12, 10))
        tk.Label(
            info,
            text="Hover over entry boxes for help.",
            font=(FONT_FAMILY, 9),
            fg=ENTERPRISE_TEXT,
            bg=ENTERPRISE_BLUE_LIGHT,
            anchor="w",
        ).pack(fill="x", padx=12, pady=9)

        body = tk.Frame(self.host, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        form_outer = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        form_outer.grid(row=0, column=0, sticky="nsew")
        form_outer.grid_rowconfigure(0, weight=1)
        form_outer.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(
            form_outer,
            bg=WHITE,
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(
            form_outer,
            orient="vertical",
            command=canvas.yview,
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        form = tk.Frame(canvas, bg=WHITE)
        canvas_window = canvas.create_window((0, 0), window=form, anchor="nw")
        form.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=max(event.width, form.winfo_reqwidth()),
            ),
        )
        bind_mousewheel(canvas, canvas.yview_scroll)
        bind_mousewheel(scrollbar, canvas.yview_scroll)

        self.configure_form_columns(form)
        for field_index, definition in enumerate(CONFIGURATION_FIELDS):
            row_index = field_index * 3
            self.create_field_row(form, row_index, definition)
        bind_mousewheel(form, canvas.yview_scroll)

        actions = tk.Frame(self.host, bg=BACKGROUND)
        actions.pack(fill="x", padx=18, pady=(0, 16))
        self.create_button(
            actions,
            "Cancel",
            ENTERPRISE_TEXT,
            SURFACE_MUTED,
            self.close,
            hover_background=SURFACE_HOVER,
        ).pack(side="right", padx=(8, 0))
        self.create_button(
            actions,
            "Save",
            WHITE,
            ENTERPRISE_BLUE,
            self.save,
            hover_background=PRIMARY_HOVER,
        ).pack(side="right")

    def configure_form_columns(self, form: tk.Frame) -> None:
        for column_index in range(3):
            form.grid_columnconfigure(
                column_index,
                weight=1 if column_index == 1 else 0,
                minsize=(220 if column_index == 0 else 0),
            )

    def create_field_row(
        self,
        form: tk.Frame,
        row_index: int,
        definition: Dict[str, str],
    ) -> None:
        
        # Container for field name and Mandatory/Optional tag
        label_frame = tk.Frame(form, bg=WHITE)
        
        label_frame.grid(
            row=row_index,
            column=0,
            rowspan=2,
            sticky="nw",
            padx=(12, 14),
            pady=(12, 8),
        )
        
        # Existing field name
        label = tk.Label(
            label_frame,
            text=definition["label"],
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            anchor="w",
            justify="left",
            wraplength=200,
        )
        label.pack(anchor="w")
        
        # Mandatory / Optional classification
        required = definition.get("required", False)
        
        category_text = "* Mandatory" if required else "(Optional)"
        category_color = DANGER if required else ENTERPRISE_MUTED
        
        tk.Label(
            label_frame,
            text=category_text,
            font=(FONT_FAMILY, 8),
            fg=category_color,
            bg=WHITE,
            anchor="w",
        ).pack(anchor="w", pady=(3, 0))

        entry = self.create_input_control(form)
        entry.grid(
            row=row_index,
            column=1,
            sticky="ew",
            padx=(0, 10),
            pady=(10, 3),
            ipady=6,
        )
        key = definition["key"]
        self.entries[key] = entry
        self.restore_value(key, entry)
        entry.bind("<Return>", self._save_from_event)

        label.bind(
            "<Button-1>",
            lambda event, widget=entry: widget.focus_set(),
        )

        action_frame = tk.Frame(form, bg=WHITE)
        action_frame.grid(
            row=row_index,
            column=2,
            sticky="ew",
            padx=(0, 12),
            pady=(10, 3),
        )
        if definition["control_type"] in ("file", "folder"):
            self.create_button(
                action_frame,
                "Browse",
                ENTERPRISE_BLUE,
                ENTERPRISE_BLUE_LIGHT,
                lambda field=definition, widget=entry:
                self.browse(field, widget),
            ).pack(side="left", padx=(0, 6))
        self.create_button(
            action_frame,
            "Validate" if definition["control_type"] == "text" else "Check",
            WHITE,
            ENTERPRISE_BLUE,
            lambda field=definition, widget=entry:
            self.validate_field(field, widget),
            hover_background=PRIMARY_HOVER,
        ).pack(side="left")

        status = tk.Label(
            form,
            font=(FONT_FAMILY, 8),
            bg=WHITE,
            anchor="w",
        )
        status.grid(
            row=row_index + 1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 12),
            pady=(0, 8),
        )
        self.status_labels[key] = status
        self.restore_status(key, status)

        tk.Frame(form, bg=ENTERPRISE_BORDER, height=1).grid(
            row=row_index + 2,
            column=0,
            columnspan=3,
            sticky="ew",
        )

    def create_input_control(self, parent: tk.Misc) -> tk.Entry:
        return tk.Entry(
            parent,
            font=(FONT_FAMILY, 9),
            fg=CELL_TEXT,
            bg=CELL_BG,
            relief="flat",
            bd=0,
            highlightbackground=CELL_BORDER,
            highlightcolor=CELL_FOCUS_BORDER,
            highlightthickness=1,
            insertbackground=CELL_FOCUS_BORDER,
        )

    def create_button(
        self,
        parent: tk.Misc,
        text: str,
        foreground: str,
        background: str,
        command,
        hover_background: Optional[str] = None,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            font=(FONT_FAMILY, 8, "bold"),
            fg=foreground,
            bg=background,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            padx=11,
            pady=6,
            cursor="hand2",
            command=command,
        )
        hover = hover_background or background
        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover),
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=background),
        )
        return button

    def restore_value(self, key: str, entry: tk.Entry) -> None:
        values = getattr(self.app, "settings_values", {}) or {}
        value = values.get(key, "")
        # if value:
        #     entry.insert(0, value)
        if value is not None and str(value):
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            
    def restore_status(self, key: str, label: tk.Label) -> None:
        stored = getattr(self.app, "configuration_statuses", {}).get(key, {})
        if isinstance(stored, dict):
            text = stored.get("text", STATUS_TEXT)
            kind = stored.get("kind", STATUS_NEUTRAL)
        else:
            text = STATUS_TEXT
            kind = STATUS_NEUTRAL
        self.status_values[key] = {"text": text, "kind": kind}
        self.set_status_style(label, text, kind)

    def set_status_style(self, label: tk.Label, text: str, kind: str) -> None:
        colors = {
            STATUS_NEUTRAL: ENTERPRISE_MUTED,
            STATUS_SUCCESS: SUCCESS,
            STATUS_WARNING: STATUS_WARNING_COLOR,
            STATUS_ERROR: DANGER,
        }
        label.configure(text=text, fg=colors.get(kind, ENTERPRISE_MUTED))

    def set_status(self, key: str, text: str, kind: str) -> None:
        self.status_values[key] = {"text": text, "kind": kind}
        self.set_status_style(self.status_labels[key], text, kind)

    def browse(self, definition: Dict[str, str], entry: tk.Entry) -> None:
        picker_title = f"Select {definition['label']}"
        if definition["control_type"] == "folder":
            path = filedialog.askdirectory(
                parent=self.window,
                title=picker_title,
            )
        else:
            path = filedialog.askopenfilename(
                parent=self.window,
                title=picker_title,
            )
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)
            self.set_status(definition["key"], "Ready to check", STATUS_NEUTRAL)

    def validate_field(
        self,
        definition: Dict[str, str],
        entry: tk.Entry,
    ) -> None:
        key = definition["key"]
        value = entry.get().strip()
        control_type = definition["control_type"]

        if control_type == "text":
            if value:
                self.set_status(
                    key,
                    "⚠ License validity cannot be automatically verified",
                    STATUS_WARNING,
                )
            else:
                self.set_status(key, "✗ License key is empty", STATUS_ERROR)
            return

        if control_type == "folder":
            if os.path.isdir(value):
                self.set_status(
                    key,
                    "✓ Directory found and validated",
                    STATUS_SUCCESS,
                )
            else:
                self.set_status(key, "✗ Directory not found", STATUS_ERROR)
            return

        if os.path.isfile(value):
            self.set_status(
                key,
                "✓ File found and validated",
                STATUS_SUCCESS,
            )
        else:
            self.set_status(key, "✗ File not found", STATUS_ERROR)

    def save(self) -> None:
        missing_fields = []
        
        # Check all mandatory configuration fields
        for definition in CONFIGURATION_FIELDS:
            if not definition.get("required", False):
                continue
            
            key = definition["key"]
            value = self.entries[key].get().strip()
            
            if not value:
                missing_fields.append(definition["label"])
                
        # Display warning if mandatory fields are empty
        if missing_fields:
            messagebox.showwarning(
                "Mandatory Fields Missing",
                "Please fill the mandatory fields.\n\n"
                + "\n".join(missing_fields),
                parent=self.window,
            )
            return
        
        # Existing save functionality
        self.app.settings_values.update(
            {
                key: entry.get().strip()
                for key, entry in self.entries.items()
            }
        )
        
        self.app.configuration_statuses = {
            key: dict(value)
            for key, value in self.status_values.items()
        }
        
        messagebox.showinfo(
            "Configuration Saved",
            "Configuration saved successfully.",
            parent=self.window,
        )
        # if not self.embedded:
        #     self.close()

        # Close the complete Settings dialog after successful save
        if self.embedded:
            self.app.close_child_window("Settings")
        else:
            self.close()
        
    def _close_from_event(self, event=None):
        self.close()
        return "break"

    def _save_from_event(self, event=None):
        self.save()
        return "break"

    def center_window(self, parent: tk.Misc) -> None:
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = max(0, int((screen_width - width) / 2))
        y = max(0, int((screen_height - height) / 2))
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def close(self) -> None:
        if self.embedded:
            # The combined Settings window owns its own lifetime.
            notebook = self.host.master.master
            if isinstance(notebook, ttk.Notebook):
                notebook.select(0)
            return
        if self.closed:
            return
        self.closed = True
        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        child_windows = getattr(self.app, "child_windows", {})
        if child_windows.get(self.window_key) is self.window:
            child_windows.pop(self.window_key, None)
        if self.window.winfo_exists():
            self.window.destroy()

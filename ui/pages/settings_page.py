"""Settings page for the application menu."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

from pathlib import Path
from utils.constants import *
from ui.widgets.mousewheel import bind_mousewheel


BASIC_SETTINGS = (
    {
        "description": "Path to Python executable",
        "name": "path_to_python_executable",
        "input_type": "File Picker",
        "picker_type": "file",
        "required": True,
    },
    {
        "description": "Folder containing run_saw.py",
        "name": "folder_containing_run_saw_py",
        "input_type": "File Picker",
        "picker_type": "folder",
        "required": True,
    },
    {
        "description": "Material Library Path",
        "name": "material_path",
        "input_type": "File Picker",
        "picker_type": "folder",
        "required": True,
    },
    {
        "description": "Template Library Path",
        "name": "template_path",
        "input_type": "File Picker",
        "picker_type": "folder",
        "required": True,
    },
    {
        "description": "Working Folder",
        "name": "work_dir",
        "input_type": "File Picker",
        "picker_type": "folder",
        "required": True,
    },
    {
        "description": "Output Folder",
        "name": "out_top_dir",
        "input_type": "File Picker",
        "picker_type": "folder",
        "required": True,
    },
    {
        "description": "Output Folder Structure",
        "name": "out_folder_type",
        "input_type": "Text Box",
        "required": False,
    },
)


ADVANCED_SETTINGS = (
    {
        "description": "Creep rupture fraction",
        "name": "crp_rupt_f",
        "input_type": "Text Box",
        "default_value": "1000",
        "required": False,
    },
    {
        "description": "Maximum steps",
        "name": "max_steps",
        "input_type": "Text Box",
        "default_value": "1000",
        "required": False,
    },
    {
        "description": "Minimum time increment",
        "name": "min_t_incr",
        "input_type": "Text Box",
        "default_value": "1.00E-20",
        "required": False,
    },
    {
        "description": "Strain Accuracy",
        "name": "strn_acc",
        "input_type": "Text Box",
        "default_value": "0.0001",
        "required": False,
    },
    {
        "description": "Maximum number of parallel processes",
        "name": "max_processes",
        "input_type": "Text Box",
        "default_value": "1",
        "required": False,
    },
    {
        "description": "Sc03 Elastic Timeout (seconds)",
        "name": "Sc03Elastic_timeout",
        "input_type": "Text Box",
        "default_value": "1000",
        "required": False,
    },
    {
        "description": "Sc03 Arkwright Timeout (seconds)",
        "name": "Sc03Arkwright_timeout",
        "input_type": "Text Box",
        "default_value": "1000",
        "required": False,
    },
    {
        "description": "Sc03 Arkwright Post Timeout (seconds)",
        "name": "Sc03Post_timeout",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
    {
        "description": "DARWIN Timeout (seconds)",
        "name": "CrackDarwin_timeout",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
    {
        "description": "Sk13 Timeout (seconds)",
        "name": "Sk13_timeout",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
    {
        "description": "Results Summary Timeout (seconds)",
        "name": "ResultsSummary_timeout",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
    {
        "description": "Sa16 Timeout (seconds)",
        "name": "CrackSa16_timeout",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
    {
        "description": "Optional Metrics File",
        "name": "metrics_file",
        "input_type": "Text Box",
        "default_value": "",
        "required": False,
    },
)


class SettingsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BACKGROUND)
        self.app = app
        self.settings_fields = {}
        self._applied_basic_paths = None
        self.build()


    def build(self):

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=20, pady=18)

        tk.Label(
            body,
            text="Application Settings",
            font=(FONT_FAMILY, 18, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
            justify="center",
            anchor="center",
        ).pack(fill="x")
        tk.Label(
            body,
            text=(
                "Configure common project details and advanced analysis "
                "locations for this SAW session."
            ),
            font=(FONT_FAMILY, 9),
            fg=SECONDARY_TEXT,
            bg=BACKGROUND,
            justify="center",
            anchor="center",
        ).pack(fill="x", pady=(4, 14))

        sections_view = tk.Frame(body, bg=BACKGROUND)
        sections_view.pack(fill="both", expand=True)
        sections_view.grid_rowconfigure(0, weight=1)
        sections_view.grid_columnconfigure(0, weight=1)

        sections_canvas = tk.Canvas(
            sections_view,
            bg=BACKGROUND,
            highlightthickness=0,
            bd=0,
        )
        sections_scroll = ttk.Scrollbar(
            sections_view,
            orient="vertical",
            command=sections_canvas.yview,
        )
        sections_canvas.configure(yscrollcommand=sections_scroll.set)
        sections_canvas.grid(row=0, column=0, sticky="nsew")
        sections_scroll.grid(row=0, column=1, sticky="ns")

        sections = tk.Frame(sections_canvas, bg=BACKGROUND)
        sections_window = sections_canvas.create_window(
            (0, 0),
            window=sections,
            anchor="nw",
        )
        sections.bind(
            "<Configure>",
            lambda event: sections_canvas.configure(
                scrollregion=sections_canvas.bbox("all")
            ),
        )
        sections_canvas.bind(
            "<Configure>",
            lambda event: sections_canvas.itemconfigure(
                sections_window,
                width=max(event.width, sections.winfo_reqwidth()),
            ),
        )

        self.create_section(
            sections,
            "Basic Settings",
            "General project and workspace information.",
            BASIC_SETTINGS,
        )
        self.create_configuration_section(sections)
        self.create_section(
            sections,
            "Advanced Settings",
            "Analysis execution and output configuration.",
            ADVANCED_SETTINGS,
        )
        bind_mousewheel(sections_canvas, sections_canvas.yview_scroll)
        bind_mousewheel(sections_scroll, sections_canvas.yview_scroll)

        actions = tk.Frame(body, bg=BACKGROUND)
        actions.pack(fill="x", pady=(14, 0))
        self.create_button(
            actions,
            "Close",
            ENTERPRISE_TEXT,
            SURFACE_MUTED,
            lambda: self.app.close_child_window("Settings"),
        ).pack(side="right", padx=(8, 0))
        self.create_button(
            actions,
            "Apply Settings",
            WHITE,
            ENTERPRISE_BLUE,
            self.apply_settings,
        ).pack(side="right")


    def create_section(self, parent, title, description, fields):
        section = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        section.pack(fill="x", pady=(0, 14))

        heading = tk.Frame(section, bg=WHITE)
        heading.pack(fill="x", padx=16, pady=(13, 8))
        tk.Label(
            heading,
            text=title,
            font=(FONT_FAMILY, 12, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
            justify="center",
        ).pack(fill="x")
        tk.Label(
            heading,
            text=description,
            font=(FONT_FAMILY, 8),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
            justify="center",
        ).pack(fill="x", pady=(3, 0))

        form = tk.Frame(section, bg=WHITE)
        form.pack(fill="x", padx=16, pady=(0, 14))
        form.grid_columnconfigure(1, weight=1)

        for row_index, field_definition in enumerate(fields):
            # required = field_definition.get("required", False)
            # category_text = " * Mandatory" if required else " (Optional)"
            # category_color = DANGER if required else ENTERPRISE_MUTED
            
            description_text = field_definition["description"]
            setting_name = field_definition["name"]
            input_type = field_definition["input_type"]

            # tk.Label(
            #     form,
            #     text=description_text,
            #     font=(FONT_FAMILY, 9, "bold"),
            #     fg=ENTERPRISE_TEXT,
            #     bg=WHITE,
            #     width=34,
            #     wraplength=280,
            #     anchor="w",
            #     justify="left",
            # ).grid(row=row_index, column=0, sticky="w", padx=(0, 12), pady=5)
            
            required = field_definition.get("required", False)
            category_text = " * Mandatory" if required else " (Optional)"
            category_color = DANGER if required else ENTERPRISE_MUTED
            
            label_frame = tk.Frame(form, bg=WHITE)
            
            label_frame.grid(
                row=row_index,
                column=0,
                sticky="w",
                padx=(0, 12),
                pady=5,
            )
            
            tk.Label(
                label_frame,
                text=description_text,
                font=(FONT_FAMILY, 9, "bold"),
                fg=ENTERPRISE_TEXT,
                bg=WHITE,
                anchor="w",
            ).pack(side="left")
            
            tk.Label(
                label_frame,
                text=category_text,
                font=(FONT_FAMILY, 8),
                fg=category_color,
                bg=WHITE,
            ).pack(side="left")

            entry = self.create_input_control(form, input_type)
            entry.grid(row=row_index, column=1, sticky="ew", ipady=6, pady=5)
            default_value = self.app.settings_values.get(
                setting_name, field_definition.get("default_value", "")
            )
            if default_value:
                entry.insert(0, default_value)
            self.settings_fields[setting_name] = entry
            if field_definition.get("required"):
                entry.bind("<KeyRelease>", self.update_configuration_enabled)
                entry.bind("<FocusOut>", self.update_configuration_enabled)

            if input_type == "File Picker":
                picker_type = field_definition.get("picker_type", "file")
                if picker_type == "folder":
                    command = lambda widget=entry: self.browse_folder(widget)
                    button_text = "Browse Folder"
                else:
                    command = lambda widget=entry: self.browse_file(widget)
                    button_text = "Browse File"
                self.create_button(
                    form,
                    button_text,
                    ENTERPRISE_BLUE,
                    ENTERPRISE_BLUE_LIGHT,
                    command,
                ).grid(row=row_index, column=2, padx=(10, 0), pady=5)

    def create_configuration_section(self, parent):
        section = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        section.pack(fill="x", pady=(0, 14))
        heading = tk.Frame(section, bg=WHITE)
        heading.pack(fill="x", padx=16, pady=(13, 8))
        tk.Label(
            heading,
            text="SAW Configuration",
            font=(FONT_FAMILY, 12, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        ).pack(fill="x")
        tk.Label(
            heading,
            text="Configure SAW tool locations and license information.",
            font=(FONT_FAMILY, 8),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
        ).pack(fill="x", pady=(3, 0))
        self.configuration_host = tk.Frame(section, bg=WHITE)
        self.configuration_host.pack(fill="x")
        from ui.dialogs.configuration_dialog import ConfigurationDialog
        self.configuration = ConfigurationDialog(
            self.winfo_toplevel(), self.app,
            embedded_parent=self.configuration_host,
        )
        self.update_configuration_enabled()

    def update_configuration_enabled(self, event=None):
        """Keep SAW controls available only while every required path is valid."""
        if not hasattr(self, "configuration_host"):
            return
        enabled = not self.validate_basic_paths()

        def set_controls(widget):
            for child in widget.winfo_children():
                if isinstance(child, (tk.Entry, tk.Button, ttk.Button)):
                    try:
                        child.configure(state="normal" if enabled else "disabled")
                    except tk.TclError:
                        pass
                set_controls(child)

        set_controls(self.configuration_host)


    def create_input_control(self, parent, input_type):
        entry_options = {
            "font": (FONT_FAMILY, 9),
            "fg": CELL_TEXT,
            "bg": CELL_BG,
            "relief": "flat",
            "highlightbackground": CELL_BORDER,
            "highlightcolor": CELL_FOCUS_BORDER,
            "highlightthickness": 1,
            "insertbackground": CELL_FOCUS_BORDER,
        }
        if input_type == "Number Input":
            entry_options["validate"] = "key"
            entry_options["validatecommand"] = (
                self.register(self.validate_number_input),
                "%P",
            )
        return tk.Entry(parent, **entry_options)


    def validate_number_input(self, proposed_value):
        if proposed_value == "":
            return True
        return re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d*)(?:[eE][+-]?\d*)?",
            proposed_value,
        ) is not None


    def create_button(self, parent, text, foreground, background, command):
        return tk.Button(
            parent,
            text=text,
            font=(FONT_FAMILY, 9, "bold"),
            fg=foreground,
            bg=background,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            command=command,
        )


    def browse_file(self, entry):
        path = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Select a file",
        )
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)
            self.update_configuration_enabled()


    def browse_folder(self, entry):
        path = filedialog.askdirectory(
            parent=self.winfo_toplevel(),
            title="Select a folder",
        )
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)
            self.update_configuration_enabled()

    def get_basic_path_values(self):
        """Return the six mandatory Basic Settings paths."""
        keys = (
            "path_to_python_executable",
            "folder_containing_run_saw_py",
            "material_path",
            "template_path",
            "work_dir",
            "out_top_dir",
        )
        return {
            key: self.settings_fields[key].get().strip()
            for key in keys
        }
        
    def validate_basic_paths(self):
        """Check all six required paths and return error messages."""
        values = self.get_basic_path_values()
        errors = []
        
        descriptions = {
            field["name"]: field["description"]
            for field in BASIC_SETTINGS
        }
        for key, value in values.items():
            label = descriptions[key]
            
            if not value:
                errors.append(f"{label}: Path is missing.")
                continue
            
            path = Path(value).expanduser()
            
            if key == "path_to_python_executable":
                if not path.is_file():
                    errors.append(
                        f"{label}: Python executable file not found."
                    )
                elif path.name.lower() not in (
                    "python.exe",
                    "pythonw.exe",
                ):
                    errors.append(
                        f"{label}: Select python.exe or pythonw.exe."
                    )
                    
            elif key == "folder_containing_run_saw_py":
                if not path.is_dir():
                    errors.append(
                        f"{label}: Folder does not exist."
                    )
                elif not (path / "run_saw.py").is_file():
                    errors.append(
                        f"{label}: run_saw.py was not found "
                        "inside the selected folder."
                    )
            else:
                if not path.is_dir():
                    errors.append(
                        f"{label}: Folder does not exist."
                    )
                    
        return errors

    def apply_settings(self):
        
        #1. Check all the mandatory fields
        missing_fields = []
        
        for field_definition in BASIC_SETTINGS + ADVANCED_SETTINGS:
            if not field_definition.get("required", False):
                continue
            
            name = field_definition["name"]
            entry = self.settings_fields.get(name)
            
            if entry is None or not entry.get().strip():
                missing_fields.append(
                    field_definition["description"]
                )
                
        if missing_fields:
            self._applied_basic_paths = None
            
            messagebox.showerror(
                "Mandatory fields missing",
                "Please fill the mandatory fields.\n\n"
                + "\n".join(missing_fields),
                parent=self.winfo_toplevel(),
            )
            return False
        
        #2. Validate actual paths and files
        path_errors = self.validate_basic_paths()
        
        if path_errors:
            self._applied_basic_paths = None
            
            messagebox.showerror(
                "Invalid Application Settings Paths",
                "The following paths are invalid:\n\n"
                +"\n".join(path_errors)
                +"\n\nPlease correct them before "
                "opening SAW configuration.",
                parent=self.winfo_toplevel(),
            )
            return False
        
        #3. Collect all settings values
        settings_values = {
            name: entry.get().strip()
            for name, entry in self.settings_fields.items()
        }
        
        old_material_path = self.app.settings_values.get("material_path", "")
        old_template_path = self.app.settings_values.get("template_path", "")

        # Preserve existing SAW configuration values
        self.app.settings_values.update(settings_values)
        
        # Backward compatibility with existing backend key
        self.app.settings_values["folder_containing_run_saw"] = (
            settings_values["folder_containing_run_saw_py"]
        )
        if old_material_path != settings_values.get("material_path", ""):
            current_page = getattr(self.app, "current_page", None)
            refresh_paths = getattr(current_page, "refresh_generated_paths", None)
            if callable(refresh_paths):
                refresh_paths(old_material_path=old_material_path)
        if old_template_path != settings_values.get("template_path", ""):
            current_page = getattr(self.app, "current_page", None)
            refresh_paths = getattr(current_page, "refresh_generated_paths", None)
            if callable(refresh_paths):
                refresh_paths(old_template_path=old_template_path)
        
        #4. Record the six successfully applied paths
        self._applied_basic_paths = self.get_basic_path_values()
        
        messagebox.showinfo(
            "Settings Applied",
            "Application settings have been applied.",
            parent=self.winfo_toplevel(),
        )
        self.update_configuration_enabled()
        return True
    
    def go_to_configuration(self):
        """Verify Application Settings before opening SAW configuration."""
        
        # Reuse existing mandatory-field and path validation
        verified = self.apply_settings()
        
        if not verified:
            return
        
        # Open SAW configuration only after successful verification
        if hasattr(self, "on_settings_verified"):
            self.on_settings_verified()
        

class CombinedSettingsPage(tk.Frame):
    """Single Application Settings page with embedded SAW configuration."""

    def __init__(self, parent, app, initial_tab="settings"):
        super().__init__(parent, bg=BACKGROUND)
        
        self.application_settings = SettingsPage(self, app)
        self.application_settings.pack(fill="both", expand=True)
        self.configuration = self.application_settings.configuration
        self.saw_settings_page = self

    def select_tab(self, name):
        """Compatibility for existing callers; settings now share one page."""
        self.application_settings.update_configuration_enabled()
            

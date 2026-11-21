"""Reusable Excel-style data editor for workflow pages."""

import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ui.widgets.mousewheel import bind_mousewheel
from ui.widgets.crack_prop_uploader import select_crack_prop_file
from utils.crack_prop_paths import (
    CRACK_PROP_FILE_COLUMNS,
    FILE_NOT_FOUND,
    file_path_colors,
    file_state_colors,
    validate_crack_prop_file,
)
from utils.constants import *


class EditDataDialog:
    def __init__(
        self,
        parent,
        module_name,
        field_definitions,
        rows,
        mode,
        on_save,
        on_close,
        form_header=None,
        header_groups=None,
        material_path_getter=None,
    ):
        self.module_name = module_name
        self.form_header = form_header or module_name
        self.field_definitions = [dict(field) for field in field_definitions]
        self.headers = [field["label"] for field in self.field_definitions]
        self.initial_rows = [list(row) for row in rows]
        self.mode = mode
        self.numeric_popup = (
            module_name == "Crack Geom Material" and mode == "new"
        )
        self.material_path_getter = material_path_getter
        self.on_save = on_save
        self.on_close = on_close
        self.header_groups = tuple(header_groups or ())
        self.entries = []
        self.row_labels = []
        self.closed = False
        self.scroll_canvas: tk.Canvas |  None = None
        self.header_row_count = 2 if self.header_groups else 1

        self.window = tk.Toplevel(parent)
        self.dialog_title = (
            "Add New Data" if mode == "new" else "Update Existing Data"
        )
        self.window.title(f"SAW | {self.dialog_title} - {module_name}")

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        dialog_width = min(1200, max(760, screen_width - 80))
        dialog_height = min(680, max(480, screen_height - 120))
        self.window.geometry(f"{dialog_width}x{dialog_height}")
        self.window.minsize(
            min(900, dialog_width),
            min(500, dialog_height),
        )
        self.window.configure(bg=BACKGROUND)
        self.window.resizable(True, True)
        self.window.overrideredirect(False)
        try:
            self.window.wm_attributes("-toolwindow", False)
        except tk.TclError:
            pass

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.center_window(parent)
        self.build()


    def center_window(self, parent):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")


    def build(self):
        header = tk.Frame(self.window, bg=ENTERPRISE_BLUE, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_block = tk.Frame(header, bg=ENTERPRISE_BLUE)
        title_block.pack(side="left", fill="both", expand=True, padx=22)

        tk.Label(
            title_block,
            text=self.dialog_title,
            font=(FONT_FAMILY, 16, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
        ).pack(anchor="w", pady=(14, 0))

        tk.Label(
            title_block,
            text=self.form_header,
            font=(FONT_FAMILY, 9),
            fg=DIALOG_SUBTEXT,
            bg=ENTERPRISE_BLUE,
        ).pack(anchor="w")

        header_meta = tk.Frame(header, bg=ENTERPRISE_BLUE)
        header_meta.pack(side="right", padx=22)
        tk.Label(
            header_meta,
            text="EDIT MODE",
            font=(FONT_FAMILY, 8, "bold"),
            fg=WHITE,
            bg=EDIT_HEADER_ACCENT,
            padx=10,
            pady=5,
        ).pack(anchor="e")
        tk.Label(
            header_meta,
            text=f"{len(self.headers)} fields",
            font=(FONT_FAMILY, 8),
            fg=DIALOG_SUBTEXT,
            bg=ENTERPRISE_BLUE,
        ).pack(anchor="e", pady=(4, 0))

        instruction = tk.Frame(
            self.window,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        instruction.pack(fill="x", padx=18, pady=(12, 10))

        tk.Frame(instruction, bg=EDIT_HEADER_ACCENT, width=4).pack(
            side="left", fill="y"
        )

        tk.Label(
            instruction,
            text="Data Entry Workspace",
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        ).pack(side="left", padx=12, pady=10)

        body = tk.Frame(self.window, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        grid_outer = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            bd=0,
            padx=1,
            pady=1,
        )
        grid_outer.grid(row=0, column=0, sticky="nsew", pady=(0, 12))

        canvas = tk.Canvas(grid_outer, bg=WHITE, highlightthickness=0)
        vertical_scroll = ttk.Scrollbar(
            grid_outer, orient="vertical", command=canvas.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            grid_outer, orient="horizontal", command=canvas.xview
        )
        canvas.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )
        canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")
        grid_outer.grid_rowconfigure(0, weight=1)
        grid_outer.grid_columnconfigure(0, weight=1)

        grid = tk.Frame(canvas, bg=WHITE)
        canvas_window = canvas.create_window((0, 0), window=grid, anchor="nw")
        grid.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: self.resize_canvas(canvas, canvas_window, event),
        )

        self.create_headers(grid)
        self.scroll_canvas = canvas

        existing_rows = self.initial_rows if self.mode == "update" else []
        if existing_rows:
            for row in existing_rows:
                self.add_row(grid, row)
        else:
            self.add_row(grid)
        bind_mousewheel(canvas, canvas.yview_scroll)
        bind_mousewheel(grid, canvas.yview_scroll)
        bind_mousewheel(vertical_scroll, canvas.yview_scroll)

        controls = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            padx=12,
            pady=10,
        )
        controls.grid(row=1, column=0, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        left_controls = tk.Frame(controls, bg=WHITE)
        left_controls.grid(row=0, column=0, sticky="w")

        self.create_button(
            left_controls,
            "+  Add Record",
            ENTERPRISE_BLUE,
            ENTERPRISE_BLUE_LIGHT,
            lambda: self.add_row(grid),
            hover_background=PRIMARY_LIGHT,
        ).pack(side="left", padx=(0, 8))

        self.create_button(
            left_controls,
            "Remove Row",
            DANGER,
            DANGER_LIGHT,
            lambda: self.delete_selected_row(),
            hover_background=DANGER_HOVER,
        ).pack(side="left")

        status_controls = tk.Frame(controls, bg=WHITE)
        status_controls.grid(row=0, column=1, sticky="w", padx=12)

        self.record_label = tk.Label(
            status_controls,
            text=f"Records: {len(self.entries)}",
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        )
        self.record_label.pack(side="left")

        self.status_label = tk.Label(
            status_controls,
            text="Ready for data entry",
            font=(FONT_FAMILY, 8),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
        )
        self.status_label.pack(side="left", padx=(12, 0))

        right_controls = tk.Frame(controls, bg=WHITE)
        right_controls.grid(row=0, column=2, sticky="e", padx=10)

        self.create_button(
            right_controls,
            "Cancel",
            ENTERPRISE_TEXT,
            SURFACE_MUTED,
            self.close,
            hover_background=SURFACE_HOVER,
        ).pack(side="left", padx=(0, 8))

        self.create_button(
            right_controls,
            "Save & Close",
            WHITE,
            ENTERPRISE_BLUE,
            self.apply,
            hover_background=PRIMARY_HOVER,
        ).pack(side="left")

        if self.entries and self.entries[0]:
            self.entries[0][0].focus_set()


    def create_button(
        self,
        parent,
        text,
        foreground,
        background,
        command,
        hover_background=None,
    ):
        button = tk.Button(
            parent,
            text=text,
            font=(FONT_FAMILY, 9, "bold"),
            fg=foreground,
            bg=background,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=command,
        )
        hover_background = hover_background or background
        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover_background),
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=background),
        )
        return button


    def create_headers(self, grid):
        header_row = 1 if self.header_groups else 0
        corner_frame = tk.Frame(grid, padx=1, pady=1, bg=ENTERPRISE_BORDER)
        corner_frame.grid(
            row=0,
            column=0,
            rowspan=2 if self.header_groups else 1,
            sticky="nsew",
            padx=(0, 1),
            pady=(0, 1),
        )
        tk.Label(
            corner_frame,
            text="#",
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=TABLE_HEADER,
            width=5,
            padx=5,
            pady=8,
        ).pack(fill="both", expand=True)

        if self.header_groups:
            for group in self.header_groups:
                start = group["start"] + 1
                span = group["span"]
                label = group["label"]
                is_empty = not label
                group_frame = tk.Frame(
                    grid,
                    bg=GROUP_HEADER if not is_empty else GROUP_HEADER_EMPTY,
                    padx=1,
                    pady=1,
                    highlightbackground=ENTERPRISE_BORDER,
                    highlightthickness=1,
                )
                group_frame.grid(
                    row=0,
                    column=start,
                    columnspan=span,
                    sticky="nsew",
                    padx=1,
                    pady=(0, 1),
                )
                tk.Label(
                    group_frame,
                    text=label,
                    font=(FONT_FAMILY, 8, "bold"),
                    fg=(WHITE if self.mode == "new" else "black"),
                    bg=GROUP_HEADER if not is_empty else GROUP_HEADER_EMPTY,
                    anchor="center",
                    padx=7,
                    pady=5,
                ).pack(fill="both", expand=True)

        for index, header in enumerate(self.headers):
            header_frame = tk.Frame(
                grid, bg=ENTERPRISE_BORDER, padx=1, pady=1
            )
            header_frame.grid(
                row=header_row,
                column=index + 1,
                sticky="nsew",
                padx=1,
                pady=(0, 1),
            )
            tk.Label(
                header_frame,
                text=header,
                font=(FONT_FAMILY, 8, "bold"),
                fg=ENTERPRISE_TEXT,
                    bg=TABLE_HEADER,
                width=17,
                anchor="center",
                justify="center",
                wraplength=130,
                padx=7,
                pady=8,
            ).pack(fill="both", expand=True)
            
            required = self.field_definitions[index].get(
                "required",
                False,
            )
            category_text = (
                "* Mandatory" if required else "(Optional)"
            )
            category_color = (
                DANGER if required else ENTERPRISE_MUTED
            )
            tk.Label(
                header_frame,
                text=category_text,
                font=(FONT_FAMILY, 8),
                fg=category_color,
                bg=TABLE_HEADER,
                anchor="center",
                pady=3,
            ).pack(fill="x")

        for index in range(len(self.headers) + 1):
            grid.grid_columnconfigure(index, weight=1)


    def add_row(self, grid, values=None):
        row_number = len(self.entries) + 1
        values = list(values) if values else []
        values += [""] * max(0, len(self.headers) - len(values))
        row_bg = CELL_ALT_BG if row_number % 2 == 0 else CELL_BG
        row_entries = []

        number_label = tk.Label(
            grid,
            text=str(row_number),
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_MUTED,
            bg=row_bg,
            width=5,
            padx=5,
            pady=6,
        )
        number_label.grid(
            row=row_number + self.header_row_count - 1,
            column=0,
            sticky="nsew",
            padx=(0, 1),
            pady=1,
        )

        for column_index, header in enumerate(self.headers):
            cell_frame = tk.Frame(
                grid, bg=CELL_BORDER, padx=1, pady=1
            )
            cell_frame.grid(
                row=row_number + self.header_row_count - 1,
                column=column_index + 1,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            value = values[column_index]
            field_definition = self.field_definitions[column_index]
            input_type = field_definition["input_type"]

            if input_type in ("Dropdown", "Yes/No Dropdown"):
                entry = ttk.Combobox(
                    cell_frame,
                    values=list(field_definition.get("options", ())),
                    state="readonly",
                    font=(FONT_FAMILY, 9),
                    width=18,
                )
                entry.pack(fill="both", expand=True, ipady=4, padx=3)
                entry.set(value)
                entry._is_dropdown = True
            elif input_type in ("File Picker", "File Upload"):
                control_frame = tk.Frame(cell_frame, bg=row_bg)
                control_frame.pack(fill="both", expand=True)
                entry = tk.Entry(
                    control_frame,
                    font=(FONT_FAMILY, 9),
                    fg=CELL_TEXT,
                    bg=row_bg,
                    relief="flat",
                    bd=0,
                    width=14,
                    insertbackground=CELL_FOCUS_BORDER,
                    highlightthickness=0,
                    justify="left",
                )
                entry.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    ipady=6,
                    padx=(3, 1),
                )
                if value:
                    entry.insert(0, value)
                if (
                    self.module_name == "Crack Prop Material"
                    and column_index in {
                        index for index, _, _ in CRACK_PROP_FILE_COLUMNS
                    }
                ):
                    entry.configure(state="readonly")
                    entry.bind(
                        "<Button-1>",
                        lambda event, widget=entry:
                        self.open_file_picker_from_cell(widget),
                    )
                    cell_frame.bind(
                        "<Button-1>",
                        lambda event, widget=entry:
                        self.open_file_picker_from_cell(widget),
                    )
                self.create_file_button(
                    control_frame,
                    entry,
                    field_definition.get("picker_type", "file"),
                ).pack(side="right", padx=(1, 2), pady=2)
                entry._is_dropdown = False
                self.bind_text_entry(entry, row_bg)
            else:
                entry_options = {
                    "font": (FONT_FAMILY, 9),
                    "fg": CELL_TEXT,
                    "bg": row_bg,
                    "relief": "flat",
                    "bd": 0,
                    "width": 18,
                    "insertbackground": CELL_FOCUS_BORDER,
                    "highlightthickness": 0,
                    "justify": "left",
                }
                if input_type == "Number Field" or (
                    self.numeric_popup
                    and field_definition["label"] not in {
                        "Crack Def",
                        "Crack Name",
                        "Template Name",
                        "DARWIN crack type",
                    }
                ):
                    entry_options["validate"] = "key"
                    entry_options["validatecommand"] = (
                        self.window.register(self.validate_number_input),
                        "%P",
                    )
                entry = tk.Entry(cell_frame, **entry_options)
                entry.pack(fill="both", expand=True, ipady=6, padx=3)
                if value:
                    entry.insert(0, value)
                entry._is_dropdown = False
                self.bind_text_entry(entry, row_bg)

            entry._cell_frame = cell_frame
            entry._column_index = column_index
            entry._row_index = row_number - 1
            entry.bind(
                "<Return>",
                lambda event, widget=entry: self.focus_next(widget),
            )
            row_entries.append(entry)

            if self.module_name == "Crack Prop Material" and column_index < 3:
                entry.bind(
                    "<KeyRelease>",
                    lambda event, cells=row_entries:
                    self.on_crack_prop_source_changed(cells),
                    add="+",
                )

        self.entries.append(row_entries)
        self.row_labels.append(number_label)
        if self.scroll_canvas is not None:
            bind_mousewheel(grid, self.scroll_canvas.yview_scroll)
        self.record_label_update("New row added - enter the required values")
        if self.module_name == "Crack Prop Material":
            self.regenerate_crack_prop_row(
                row_entries,
                replace=self.mode == "new",
            )
            snapshot = tuple(entry.get().strip() for entry in row_entries[:3])
            for entry in row_entries[:3]:
                entry._path_source_snapshot = snapshot


    def on_crack_prop_source_changed(self, row_entries):
        """Regenerate paths only when a source value actually changed."""
        current = tuple(entry.get().strip() for entry in row_entries[:3])
        previous = getattr(row_entries[0], "_path_source_snapshot", None)
        if current == previous:
            return
        self.regenerate_crack_prop_row(row_entries, replace=True)
        for entry in row_entries[:3]:
            entry._path_source_snapshot = current


    def bind_text_entry(self, entry, row_bg):
        entry.bind(
            "<FocusIn>",
            lambda event, widget=entry: self.focus_in(widget),
            add="+",
        )
        entry.bind(
            "<FocusOut>",
            lambda event, widget=entry, bg=row_bg:
            self.focus_out(widget, bg),
            add="+",
        )


    def create_file_button(self, parent, entry, picker_type):
        return tk.Button(
            parent,
            text="...",
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_BLUE,
            bg=ENTERPRISE_BLUE_LIGHT,
            activebackground=ENTERPRISE_BLUE_LIGHT,
            activeforeground=ENTERPRISE_BLUE,
            relief="flat",
            bd=0,
            width=3,
            cursor="hand2",
            command=lambda: self.select_path(entry, picker_type),
        )


    def select_path(self, entry, picker_type):
        if (
            self.module_name == "Crack Prop Material"
            and entry._column_index in {
                index for index, _, _ in CRACK_PROP_FILE_COLUMNS
            }
        ):
            row = self.entries[entry._row_index]
            path = select_crack_prop_file(
                self.window,
                row[0].get().strip(),
                entry._column_index,
            )
        elif picker_type == "folder":
            path = filedialog.askdirectory(
                parent=self.window,
                title="Select a folder",
            )
        else:
            path = filedialog.askopenfilename(
                parent=self.window,
                title="Select a file",
            )
        if path:
            self.set_entry_value(entry, path)
            if (
                self.module_name == "Crack Prop Material"
                and entry._column_index in {
                    index for index, _, _ in CRACK_PROP_FILE_COLUMNS
                }
            ):
                self.set_file_path_status(entry, path)

    def open_file_picker_from_cell(self, entry):
        self.select_path(entry, "file")
        return "break"

    @staticmethod
    def set_entry_value(entry, value):
        read_only = entry.cget("state") == "readonly"
        if read_only:
            entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        if read_only:
            entry.configure(state="readonly")

    def set_file_path_status(self, entry, path):
        row_index = getattr(entry, "_row_index", None)
        column_index = getattr(entry, "_column_index", None)
        material = ""
        if row_index is not None and row_index < len(self.entries):
            material = self.entries[row_index][0].get().strip()
        background, foreground = file_state_colors(
            path, material, column_index
        )
        entry._file_status_bg = background
        entry.configure(
            bg=background,
            fg=foreground,
            justify="center" if path == "Not found" else "left",
        )
        entry._cell_frame.configure(bg=background)

    def regenerate_crack_prop_row(self, row_entries, replace=False):
        """Populate expected file paths for this row and update cell status."""
        if self.module_name != "Crack Prop Material":
            return
        from utils.crack_prop_paths import build_crack_prop_file_paths

        material_path = (
            self.material_path_getter()
            if self.material_path_getter is not None
            else ""
        )
        row_values = [entry.get().strip() for entry in row_entries[:3]]
        paths = build_crack_prop_file_paths(material_path, row_values)
        for path, (column_index, _, _) in zip(paths, CRACK_PROP_FILE_COLUMNS):
            entry = row_entries[column_index]
            current = entry.get().strip()
            expected_exists = (
                path != FILE_NOT_FOUND
                and file_path_colors(path, row_values[0], column_index)[0]
                == SUCCESS
            )
            if replace:
                display_value = path if expected_exists else FILE_NOT_FOUND
            elif (
                current != FILE_NOT_FOUND
                and validate_crack_prop_file(
                    current, row_values[0], column_index
                ) is None
            ):
                # A stored valid path represents a previously accepted cell.
                # Do not recheck disk presence just because the uploader opened.
                display_value = current
            else:
                display_value = path if expected_exists else FILE_NOT_FOUND
            self.set_entry_value(entry, display_value)
            self.set_file_path_status(entry, display_value)


    def validate_number_input(self, proposed_value):
        if proposed_value == "":
            return True
        return re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d*)(?:[eE][+-]?\d*)?",
            proposed_value,
        ) is not None

    def is_valid_numeric_value(self, value):
        """Validate a completed numeric value for Add New popup fields."""
        return bool(value.strip()) and re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
            value.strip(),
        ) is not None


    def record_label_update(self, status):
        if hasattr(self, "record_label"):
            self.record_label.configure(text=f"Records: {len(self.entries)}")
        if hasattr(self, "status_label"):
            self.status_label.configure(text=status)


    def focus_in(self, widget):
        widget._cell_frame.configure(bg=CELL_FOCUS_BORDER, padx=2, pady=2)
        widget.configure(bg=CELL_FOCUS_BG)


    def focus_out(self, widget, original_bg):
        widget._cell_frame.configure(bg=CELL_BORDER, padx=1, pady=1)
        status_bg = getattr(widget, "_file_status_bg", None)
        if status_bg:
            widget.configure(bg=status_bg, fg=WHITE)
        else:
            widget.configure(bg=original_bg)


    def focus_next(self, widget):
        for row_index, row in enumerate(self.entries):
            for column_index, cell in enumerate(row):
                if cell is widget:
                    if column_index + 1 < len(row):
                        row[column_index + 1].focus_set()
                    elif row_index + 1 < len(self.entries):
                        self.entries[row_index + 1][0].focus_set()
                    return "break"


    def delete_selected_row(self):
        focused_widget = self.window.focus_get()
        selected_row = None
        for index, row in enumerate(self.entries):
            if focused_widget in row:
                selected_row = index
                break

        if selected_row is None:
            if not self.entries:
                return
            selected_row = len(self.entries) - 1

        for widget in self.entries[selected_row]:
            widget._cell_frame.destroy()
        self.row_labels[selected_row].destroy()
        del self.entries[selected_row]
        del self.row_labels[selected_row]

        for index, row in enumerate(self.entries):
            row_number = index + 1
            for widget in row:
                widget._row_index = index
            self.row_labels[index].configure(text=str(row_number))
            self.row_labels[index].grid_configure(
                row=row_number + self.header_row_count - 1
            )
            row_bg = CELL_ALT_BG if row_number % 2 == 0 else CELL_BG
            for widget in row:
                widget._cell_frame.grid_configure(
                    row=row_number + self.header_row_count - 1
                )
                if not getattr(widget, "_is_dropdown", False):
                    widget.configure(bg=row_bg)

        self.record_label_update("Selected row removed")
        if self.entries:
            self.entries[min(selected_row, len(self.entries) - 1)][0].focus_set()


    def resize_canvas(self, canvas, canvas_window, event):
        grid = canvas.nametowidget(canvas.itemcget(canvas_window, "window"))
        requested_width = grid.winfo_reqwidth()
        canvas.itemconfigure(canvas_window, width=max(event.width, requested_width))


    def apply(self):
        if self.numeric_popup:
            invalid = []
            string_fields = {
                "Crack Def", "Crack Name", "Template Name",
                "DARWIN crack type",
            }
            for row_number, row_entries in enumerate(self.entries, start=1):
                for definition, entry in zip(self.field_definitions, row_entries):
                    value = entry.get().strip()
                    if (
                        definition["label"] not in string_fields
                        and value
                        and not self.is_valid_numeric_value(value)
                    ):
                        invalid.append(
                            f"Row {row_number}: {definition['label']}"
                        )
            if invalid:
                messagebox.showwarning(
                    "Invalid Numeric Values",
                    "Enter an integer or decimal number in these fields.\n\n"
                    + "\n".join(invalid),
                    parent=self.window,
                )
                return

        rows = []
        for row_entries in self.entries:
            values = []
            for entry in row_entries:
                value = entry.get().strip()
                values.append(value)
            if any(values):
                rows.append(values)

        if not rows:
            messagebox.showwarning(
                "No Data",
                "Please enter at least one row of data.",
                parent=self.window,
            )
            return
        
        missing = []
        
        for row_number, values in enumerate(rows, start=1):
            for index, definition in enumerate(self.field_definitions):
                if definition.get("required", False) and (
                    index >= len(values)
                    or not str(values[index]).strip()
                ):
                    missing.append(
                        f"Row {row_number}: {definition['label']}"
                    )
        if missing:
            messagebox.showwarning(
                "Mandatory Fields Missing",
                "Please fill the mandatory fields.\n\n"
                + "\n".join(missing),
                parent=self.window,
            )
            return

        self.on_save(rows, self.mode)
        self.close()


    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.window.winfo_exists():
            self.window.destroy()
        self.on_close()

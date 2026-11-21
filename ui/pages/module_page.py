"""Shared workflow page foundation used by each module-specific page."""

import tkinter as tk
from tkinter import messagebox, ttk

from ui.dialogs.edit_data_dialog import EditDataDialog
from ui.widgets.mousewheel import bind_mousewheel
from utils.constants import *
from validation.registry import VALIDATOR_REGISTRY


class ModulePage(tk.Frame):
    module_name = ""
    header_label = ""
    description = ""
    column_headers = ()
    field_definitions = ()
    header_groups = ()
    dropdown_column = ""
    dropdown_options = ()

    def __init__(self, parent, app):
        super().__init__(parent, bg=BACKGROUND)
        self.app = app
        self.current_tree = None
        self.progress = None
        self.progress_label = None
        self.validator = VALIDATOR_REGISTRY[self.module_name]
        self.build()


    def build(self):
        module_header = tk.Frame(self, bg=BACKGROUND)
        module_header.pack(fill="x")
        module_header.grid_columnconfigure(0, weight=1)
        module_header.grid_columnconfigure(2, weight=1)

        title_area = tk.Frame(module_header, bg=BACKGROUND)
        title_area.grid(row=0, column=1)

        tk.Label(
            title_area,
            text=self.header_label or self.module_name,
            font=(FONT_FAMILY, 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
            justify="center",
        ).pack(anchor="center")

        tk.Label(
            title_area,
            text=self.description,
            font=(FONT_FAMILY, 9),
            fg=SECONDARY_TEXT,
            bg=BACKGROUND,
            justify="center",
        ).pack(anchor="center", pady=(3, 0))

        add_button = self.create_action_button(
            module_header,
            "Add New",
            WHITE,
            ENTERPRISE_BLUE,
            self.open_add_new,
        )
        add_button.grid(row=0, column=2, sticky="e", pady=5)

        workspace = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        workspace.pack(fill="both", expand=True, pady=(18, 12))

        table_frame = tk.Frame(workspace, bg=WHITE)
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)
        tree_container = tk.Frame(table_frame, bg=WHITE)
        tree_container.pack(fill="both", expand=True)
        tree_container.grid_columnconfigure(0, weight=1)

        y_scroll = ttk.Scrollbar(tree_container, orient="vertical")
        self.vertical_scrollbar = y_scroll
        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal")
        self.horizontal_scrollbar = x_scroll

        self.column_ids = tuple(
            f"column_{index}" for index in range(len(self.column_headers))
        )
        self.column_widths = [130] * len(self.column_headers)
        self.group_header = None
        if self.header_groups:
            self.create_group_header(tree_container)

        tree_row = 1 if self.header_groups else 0

        tree_style = ttk.Style(self)
        tree_style.configure(
            "SAW.Treeview",
            font=(FONT_FAMILY, 9),
            rowheight=28,
        )
        tree_style.configure(
            "SAW.Treeview.Heading",
            background=ENTERPRISE_BLUE_LIGHT,
            foreground=ENTERPRISE_TEXT,
            font=(FONT_FAMILY, 8, "bold"),
        )

        self.current_tree = ttk.Treeview(
            tree_container,
            columns=self.column_ids,
            show="headings",
            selectmode="browse",
            style="SAW.Treeview",
            yscrollcommand=self.sync_vertical_scroll,
            xscrollcommand=self.sync_horizontal_scroll,
        )
        y_scroll.config(command=self.current_tree.yview)
        x_scroll.config(command=self.current_tree.xview)

        for index, (column_id, header) in enumerate(
            zip(self.column_ids, self.column_headers)
        ):
            self.current_tree.heading(column_id, text=header)
            self.current_tree.column(
                column_id,
                width=self.column_widths[index],
                minwidth=100,
                anchor="center" if self.header_groups else "w",
            )

        self.current_tree.grid(row=tree_row, column=0, sticky="nsew")
        y_scroll.grid(row=tree_row, column=1, sticky="ns")
        x_scroll.grid(row=tree_row + 1, column=0, sticky="ew")
        tree_container.grid_rowconfigure(tree_row, weight=1)
        bind_mousewheel(self.current_tree, self.current_tree.yview_scroll)
        bind_mousewheel(y_scroll, self.current_tree.yview_scroll)

        action_bar = tk.Frame(workspace, bg=WHITE)
        action_bar.pack(fill="x", padx=12, pady=(0, 12))

        self.create_action_button(
            action_bar,
            "Update Existing",
            WHITE,
            ENTERPRISE_BLUE,
            self.open_update_existing,
        ).pack(side="left", padx=(8, 0))

        self.create_action_button(
            action_bar,
            "Submit",
            WHITE,
            SUCCESS,
            self.submit_data,
        ).pack(side="right")

        progress_area = tk.Frame(self, bg=BACKGROUND)
        progress_area.pack(fill="x")

        tk.Label(
            progress_area,
            text="Progress",
            font=(FONT_FAMILY, 8, "bold"),
            fg=SECONDARY_TEXT,
            bg=BACKGROUND,
        ).pack(side="left", padx=(0, 8))

        self.progress = ttk.Progressbar(
            progress_area,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.progress_label = tk.Label(
            progress_area,
            text="0%",
            font=(FONT_FAMILY, 8, "bold"),
            fg=SECONDARY_TEXT,
            bg=BACKGROUND,
            width=5,
        )
        self.progress_label.pack(side="right")
        self.refresh_table()


    def create_group_header(self, parent):
        """Render optional Excel-style grouped headers above the table."""

        total_width = sum(self.column_widths)
        group_header = tk.Canvas(
            parent,
            height=28,
            bg=WHITE,
            highlightthickness=0,
            bd=0,
        )
        group_header.grid(row=0, column=0, sticky="ew")
        group_header.configure(scrollregion=(0, 0, total_width, 28))

        group_surface = tk.Frame(
            group_header,
            bg=WHITE,
            width=total_width,
            height=28,
        )
        group_surface.pack_propagate(False)
        group_header.create_window(
            (0, 0),
            window=group_surface,
            anchor="nw",
        )

        for group_index, group in enumerate(self.header_groups):
            start = group["start"]
            span = group["span"]
            width = sum(self.column_widths[start:start + span])
            offset = sum(self.column_widths[:start])
            label = group["label"]
            is_empty = not label
            tk.Label(
                group_surface,
                text=label,
                font=(FONT_FAMILY, 9, "bold"),
                fg=WHITE if not is_empty else ENTERPRISE_MUTED,
                bg=GROUP_HEADER if not is_empty else GROUP_HEADER_EMPTY,
                anchor="center",
                padx=8,
                pady=5,
            ).place(x=offset, y=0, width=width, height=28)
            if group_index:
                tk.Frame(
                    group_surface,
                    bg=ENTERPRISE_BORDER,
                    width=2,
                ).place(x=offset - 1, y=0, width=2, height=28)

        self.group_header = group_header


    def sync_horizontal_scroll(self, first, last):
        """Keep the grouped header aligned with the scrollable data table."""

        if self.group_header is not None:
            self.group_header.xview_moveto(first)
        if hasattr(self, "horizontal_scrollbar"):
            self.horizontal_scrollbar.set(first, last)
        refresh_cells = getattr(self, "refresh_file_cell_overlays", None)
        if callable(refresh_cells):
            refresh_cells()


    def create_action_button(self, parent, text, foreground, background, command):
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
            padx=18,
            pady=7,
            cursor="hand2",
            command=command,
        )


    def rows(self):
        return self.app.module_data.setdefault(self.module_name, [])


    def refresh_table(self):
        if self.current_tree is None:
            return
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)
        for row in self.rows():
            values = list(row)
            values += [""] * (len(self.column_headers) - len(values))
            self.current_tree.insert(
                "", "end", values=values[:len(self.column_headers)]
            )
        refresh_cells = getattr(self, "refresh_file_cell_overlays", None)
        if callable(refresh_cells):
            refresh_cells()


    def sync_vertical_scroll(self, first, last):
        self.vertical_scrollbar.set(first, last)
        refresh_cells = getattr(self, "refresh_file_cell_overlays", None)
        if callable(refresh_cells):
            refresh_cells()


    def open_add_new(self):
        self.open_editor("new")


    def open_update_existing(self):
        if not self.rows():
            messagebox.showwarning(
                "No Existing Data",
                "There are no existing records to update. Use Add New first.",
                parent=self,
            )
            return
        self.open_editor("update")


    def open_editor(self, mode):
        existing = self.app.child_windows.get("edit")
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_force()
            return

        rows = self.rows() if mode == "update" else []
        self.set_progress(25)

        dialog = EditDataDialog(
            self.app.root,
            self.module_name,
            self.field_definitions,
            rows,
            mode,
            self.save_rows,
            self.close_editor,
            self.header_label or self.module_name,
            self.header_groups,
            material_path_getter=(
                lambda: (getattr(self.app, "settings_values", {}) or {}).get(
                    "material_path", ""
                )
                if self.module_name == "Crack Prop Material"
                else None
            ),
        )
        self.app.child_windows["edit"] = dialog.window


    def close_editor(self):
        self.app.child_windows.pop("edit", None)


    def save_rows(self, rows, mode):
        if mode == "new":
            self.app.module_data[self.module_name] = [
                list(row) for row in self.rows()
            ] + rows
        else:
            self.app.module_data[self.module_name] = rows
        self.app.mark_module_incomplete(self.module_name)
        self.refresh_table()
        self.set_progress(75)


    def submit_data(self):
        missing = []
        
        for row_number, row in enumerate(self.rows(), start=1):
            for index, definition in enumerate(self.field_definitions):
                if definition.get("required", False) and (
                    index >= len(row)
                    or not str(row[index]).strip()
                ):
                    missing.append(
                        f"Row {row_number}: {definition['label']}"
                    )
        if missing:
            self.app.mark_module_incomplete(self.module_name)
            
            messagebox.showwarning(
                "Mandatory Fields Missing",
                "Please fill the mandatory fields.\n\n"
                + "\n".join(missing),
                parent=self,
            )
            return
        
        result = self.validate_rows()
        if not result.is_valid:
            self.app.mark_module_incomplete(self.module_name)
            messagebox.showwarning(
                "Validation Required",
                result.message(),
                parent=self,
            )
            return

        if self.app.submit_data_for_module(self.module_name):
            self.set_progress(100)


    def validate_rows(self):
        return self.validator.validate(self.rows())


    def set_progress(self, value):
        if self.progress is None or self.progress_label is None:
            return
        self.progress["value"] = value
        self.progress_label.configure(text=f"{int(value)}%")
        self.app.root.update_idletasks()

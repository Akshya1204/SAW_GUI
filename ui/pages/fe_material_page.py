"""FE Material workflow page with row-specific item-file handling."""

import tkinter as tk
from pathlib import Path

from ui.pages.module_page import ModulePage
from ui.widgets.fe_material_uploader import select_fe_item_file
from utils.constants import FONT_FAMILY, MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS
from utils.crack_prop_paths import FILE_NOT_FOUND
from utils.fe_material_paths import (
    FE_ITEM_FILE_COLUMN,
    build_fe_item_file_path,
    fe_item_file_colors,
    validate_fe_item_file,
)
from validation.types import ValidationIssue, ValidationResult


class FEMaterialPage(ModulePage):
    module_name = "FE Material"
    description = "Manage finite-element material information."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

    def build(self):
        super().build()
        self.current_tree.bind("<Configure>", self.schedule_file_cell_overlay_refresh, add="+")
        self.current_tree.bind("<Expose>", self.schedule_file_cell_overlay_refresh, add="+")
        self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_table(self):
        material_path = (getattr(self.app, "settings_values", {}) or {}).get("material_path", "")
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            current = str(row[FE_ITEM_FILE_COLUMN]).strip()
            code = str(row[1]).strip() if len(row) > 1 else ""
            if not current or current == FILE_NOT_FOUND or validate_fe_item_file(current, code):
                expected = build_fe_item_file_path(material_path, row)
                row[FE_ITEM_FILE_COLUMN] = (
                    expected
                    if expected != FILE_NOT_FOUND
                    and validate_fe_item_file(expected, code) is None
                    and Path(expected).is_file()
                    else FILE_NOT_FOUND
                )
        super().refresh_table()

    def schedule_file_cell_overlay_refresh(self, event=None):
        if self.current_tree is not None:
            self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_file_cell_overlays(self):
        tree = self.current_tree
        if tree is None or not tree.winfo_exists():
            return
        labels = getattr(self, "_file_cell_labels", None)
        if labels is None:
            labels = self._file_cell_labels = {}
        visible = set()
        for item in tree.get_children():
            key = (item, FE_ITEM_FILE_COLUMN)
            visible.add(key)
            self.render_file_cell_overlay(item)
        for key in tuple(labels):
            if key not in visible:
                labels.pop(key).destroy()

    def render_file_cell_overlay(self, item):
        tree = self.current_tree
        values = tree.item(item, "values")
        value = str(values[FE_ITEM_FILE_COLUMN]).strip() if len(values) > FE_ITEM_FILE_COLUMN else FILE_NOT_FOUND
        code = str(values[1]).strip() if len(values) > 1 else ""
        if value != FILE_NOT_FOUND and validate_fe_item_file(value, code):
            value = FILE_NOT_FOUND
        background, foreground = fe_item_file_colors(value, code)
        key = (item, FE_ITEM_FILE_COLUMN)
        label = self._file_cell_labels.get(key)
        if label is None or not label.winfo_exists():
            label = tk.Label(tree, font=(FONT_FAMILY, 9), anchor="center", padx=5, bd=0)
            label.bind("<Button-1>", lambda event, row_id=item: self.select_file_for_cell(row_id))
            self._file_cell_labels[key] = label
        label.configure(
            text=value,
            bg=background,
            fg=foreground,
            anchor="center" if value == FILE_NOT_FOUND else "w",
        )
        bounds = tree.bbox(item, self.column_ids[FE_ITEM_FILE_COLUMN])
        if bounds:
            x, y, width, height = bounds
            label.place(x=x, y=y, width=width, height=height)
            label.lift()
        else:
            label.place_forget()

    def select_file_for_cell(self, item):
        tree = self.current_tree
        tree.selection_set(item)
        tree.focus(item)
        row_index = tree.index(item)
        rows = self.rows()
        if row_index >= len(rows):
            return "break"
        row = rows[row_index]
        code = str(row[1]).strip() if len(row) > 1 else ""
        selected_path = select_fe_item_file(self.winfo_toplevel(), code)
        if selected_path:
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            row[FE_ITEM_FILE_COLUMN] = selected_path
            self.app.mark_module_incomplete(self.module_name)
            tree.item(item, values=list(row[:len(self.column_headers)]))
            tree.update_idletasks()
            self.render_file_cell_overlay(item)
        return "break"

    def refresh_generated_paths(self, old_material_path=""):
        material_path = (getattr(self.app, "settings_values", {}) or {}).get("material_path", "")
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            old_expected = build_fe_item_file_path(old_material_path, row)
            current = str(row[FE_ITEM_FILE_COLUMN]).strip()
            code = str(row[1]).strip() if len(row) > 1 else ""
            if not current or current == FILE_NOT_FOUND or current == old_expected or validate_fe_item_file(current, code):
                expected = build_fe_item_file_path(material_path, row)
                row[FE_ITEM_FILE_COLUMN] = (
                    expected
                    if expected != FILE_NOT_FOUND and Path(expected).is_file()
                    else FILE_NOT_FOUND
                )
        super().refresh_table()

    def validate_rows(self):
        result = super().validate_rows()
        missing = tuple(
            ValidationIssue(
                row_number,
                self.column_headers[FE_ITEM_FILE_COLUMN],
                "file not found; select the file manually.",
            )
            for row_number, row in enumerate(self.rows(), start=1)
            if len(row) > FE_ITEM_FILE_COLUMN
            and (
                str(row[FE_ITEM_FILE_COLUMN]).strip() == FILE_NOT_FOUND
                or not Path(str(row[FE_ITEM_FILE_COLUMN])).is_file()
                or validate_fe_item_file(row[FE_ITEM_FILE_COLUMN], str(row[1]).strip())
            )
        )
        return ValidationResult(result.issues + missing) if missing else result

"""Template Definition page with generated, validated file cells."""

import tkinter as tk
from pathlib import Path

from ui.pages.module_page import ModulePage
from ui.widgets.template_file_uploader import select_template_file
from utils.constants import FONT_FAMILY, MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS
from utils.template_definition_paths import (
    TEMPLATE_FILE_COLUMNS,
    TEMPLATE_FILE_NOT_FOUND,
    build_template_file_paths,
    template_file_colors,
    validate_template_file,
)
from validation.types import ValidationIssue, ValidationResult


class TemplateDefinitionPage(ModulePage):
    module_name = "Template Definition"
    description = "Manage template definition data."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]
    header_groups = (
        {"label": "", "start": 0, "span": 8},
        {"label": "Darwin Template Files (3D ONLY)", "start": 8, "span": 3},
    )

    def build(self):
        super().build()
        self.current_tree.bind("<Configure>", self.schedule_file_cell_overlay_refresh, add="+")
        self.current_tree.bind("<Expose>", self.schedule_file_cell_overlay_refresh, add="+")
        self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_table(self):
        template_path = (getattr(self.app, "settings_values", {}) or {}).get("template_path", "")
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            expected_paths = build_template_file_paths(template_path, row)
            for expected, (column_index, _) in zip(expected_paths, TEMPLATE_FILE_COLUMNS):
                current = str(row[column_index]).strip()
                name = str(row[0]).strip() if row else ""
                if not current or current == TEMPLATE_FILE_NOT_FOUND or validate_template_file(current, name, column_index):
                    row[column_index] = (
                        expected
                        if expected != TEMPLATE_FILE_NOT_FOUND and Path(expected).is_file()
                        else TEMPLATE_FILE_NOT_FOUND
                    )
        super().refresh_table()

    def schedule_file_cell_overlay_refresh(self, event=None):
        if self.current_tree is not None:
            self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_file_cell_overlays(self):
        tree = self.current_tree
        if tree is None or not tree.winfo_exists():
            return
        labels = getattr(self, "_template_file_labels", None)
        if labels is None:
            labels = self._template_file_labels = {}
        visible = set()
        for item in tree.get_children():
            for column_index, _ in TEMPLATE_FILE_COLUMNS:
                key = (item, column_index)
                visible.add(key)
                self.render_file_cell_overlay(item, column_index)
        for key in tuple(labels):
            if key not in visible:
                labels.pop(key).destroy()

    def render_file_cell_overlay(self, item, column_index):
        tree = self.current_tree
        values = tree.item(item, "values")
        value = str(values[column_index]).strip() if len(values) > column_index else TEMPLATE_FILE_NOT_FOUND
        name = str(values[0]).strip() if values else ""
        if value != TEMPLATE_FILE_NOT_FOUND and validate_template_file(value, name, column_index):
            value = TEMPLATE_FILE_NOT_FOUND
        background, foreground = template_file_colors(value)
        key = (item, column_index)
        label = self._template_file_labels.get(key)
        if label is None or not label.winfo_exists():
            label = tk.Label(tree, font=(FONT_FAMILY, 9), anchor="center", padx=5, bd=0)
            label.bind(
                "<Button-1>",
                lambda event, row_id=item, col=column_index:
                self.select_file_for_cell(row_id, col),
            )
            self._template_file_labels[key] = label
        label.configure(
            text=value,
            bg=background,
            fg=foreground,
            anchor="center" if value == TEMPLATE_FILE_NOT_FOUND else "w",
        )
        bounds = tree.bbox(item, self.column_ids[column_index])
        if bounds:
            x, y, width, height = bounds
            label.place(x=x, y=y, width=width, height=height)
            label.lift()
        else:
            label.place_forget()

    def select_file_for_cell(self, item, column_index):
        tree = self.current_tree
        tree.selection_set(item)
        tree.focus(item)
        row_index = tree.index(item)
        rows = self.rows()
        if row_index >= len(rows):
            return "break"
        row = rows[row_index]
        template_path = (getattr(self.app, "settings_values", {}) or {}).get("template_path", "")
        selected_path = select_template_file(
            self.winfo_toplevel(), template_path, row, column_index
        )
        if selected_path:
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            row[column_index] = selected_path
            self.app.mark_module_incomplete(self.module_name)
            tree.item(item, values=list(row[:len(self.column_headers)]))
            tree.update_idletasks()
            self.render_file_cell_overlay(item, column_index)
        return "break"

    def refresh_generated_paths(self, old_template_path=""):
        template_path = (getattr(self.app, "settings_values", {}) or {}).get("template_path", "")
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            old_paths = build_template_file_paths(old_template_path, row)
            new_paths = build_template_file_paths(template_path, row)
            for old, expected, (column_index, _) in zip(old_paths, new_paths, TEMPLATE_FILE_COLUMNS):
                current = str(row[column_index]).strip()
                name = str(row[0]).strip()
                if not current or current == TEMPLATE_FILE_NOT_FOUND or current == old or validate_template_file(current, name, column_index):
                    row[column_index] = (
                        expected
                        if expected != TEMPLATE_FILE_NOT_FOUND and Path(expected).is_file()
                        else TEMPLATE_FILE_NOT_FOUND
                    )
        super().refresh_table()

    def validate_rows(self):
        result = super().validate_rows()
        missing = tuple(
            ValidationIssue(row_number, self.column_headers[column_index], "file not found; select the file manually.")
            for row_number, row in enumerate(self.rows(), start=1)
            for column_index, _ in TEMPLATE_FILE_COLUMNS
            if len(row) > column_index
            and (
                str(row[column_index]).strip() == TEMPLATE_FILE_NOT_FOUND
                or not Path(str(row[column_index])).is_file()
                or validate_template_file(row[column_index], str(row[0]).strip(), column_index)
            )
        )
        return ValidationResult(result.issues + missing) if missing else result

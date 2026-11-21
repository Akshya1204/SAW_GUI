"""Crack Prop Material workflow page."""

import tkinter as tk
from pathlib import Path

from ui.pages.module_page import ModulePage
from utils.constants import (
    FONT_FAMILY,
    MODULE_COLUMN_HEADERS,
    MODULE_FIELD_DEFINITIONS,
    SUCCESS,
)
from utils.crack_prop_paths import (
    CRACK_PROP_FILE_COLUMNS,
    FILE_NOT_FOUND,
    build_crack_prop_file_paths,
    file_path_colors,
    file_state_colors,
    validate_crack_prop_file,
)
from ui.widgets.crack_prop_uploader import select_crack_prop_file
from validation.types import ValidationIssue, ValidationResult


class CrackPropMaterialPage(ModulePage):
    module_name = "Crack Prop Material"
    description = "Manage crack propagation material data."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

    def build(self):
        super().build()
        self.current_tree.bind(
            "<Configure>", self.schedule_file_cell_overlay_refresh, add="+"
        )
        self.current_tree.bind(
            "<Expose>", self.schedule_file_cell_overlay_refresh, add="+"
        )
        self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_table(self):
        """Fill any unset expected-file cells before displaying saved rows."""
        material_path = (getattr(self.app, "settings_values", {}) or {}).get(
            "material_path", ""
        )
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            paths = build_crack_prop_file_paths(material_path, row)
            for path, (column_index, _, _) in zip(paths, CRACK_PROP_FILE_COLUMNS):
                current = str(row[column_index]).strip()
                material = str(row[0]).strip() if row else ""
                if (
                    not current
                    or current == FILE_NOT_FOUND
                    or validate_crack_prop_file(
                        current, material, column_index
                    ) is not None
                ):
                    row[column_index] = (
                        path
                        if path != FILE_NOT_FOUND
                        and file_path_colors(
                            path, material, column_index
                        )[0] == SUCCESS
                        else FILE_NOT_FOUND
                    )
        super().refresh_table()

    def schedule_file_cell_overlay_refresh(self, event=None):
        if self.current_tree is not None:
            self.current_tree.after_idle(self.refresh_file_cell_overlays)

    def refresh_file_cell_overlays(self):
        """Color just the six file cells in the read-only page table."""
        tree = self.current_tree
        if tree is None or not tree.winfo_exists():
            return
        labels = getattr(self, "_file_cell_labels", None)
        if labels is None:
            labels = self._file_cell_labels = {}

        visible_keys = set()
        for item in tree.get_children():
            for column_index, _, _ in CRACK_PROP_FILE_COLUMNS:
                key = (item, column_index)
                visible_keys.add(key)
                self.render_file_cell_overlay(item, column_index)

        for key in tuple(labels):
            if key not in visible_keys:
                labels.pop(key).destroy()

    def render_file_cell_overlay(self, item, column_index):
        """Paint the visible table cell from its current row value."""
        tree = self.current_tree
        values = tree.item(item, "values")
        stored_path = (
            str(values[column_index]).strip()
            if column_index < len(values) and values[column_index]
            else FILE_NOT_FOUND
        )
        material = str(values[0]).strip() if values else ""
        path = (
            stored_path
            if stored_path != FILE_NOT_FOUND
            and validate_crack_prop_file(
                stored_path, material, column_index
            ) is None
            else FILE_NOT_FOUND
        )
        background, foreground = file_state_colors(
            path, material, column_index
        )
        key = (item, column_index)
        label = self._file_cell_labels.get(key)
        if label is None or not label.winfo_exists():
            label = tk.Label(
                tree,
                font=(FONT_FAMILY, 9),
                anchor="w",
                padx=5,
                bd=0,
            )
            label.bind(
                "<Button-1>",
                lambda event, row_id=item, col_index=column_index:
                self.select_file_for_cell(row_id, col_index),
            )
            self._file_cell_labels[key] = label
        label.configure(
            text=path,
            bg=background,
            fg=foreground,
            anchor="center" if path == FILE_NOT_FOUND else "w",
        )
        bounds = tree.bbox(item, self.column_ids[column_index])
        if bounds:
            x, y, width, height = bounds
            label.place(x=x, y=y, width=width, height=height)
            label.lift()
        else:
            label.place_forget()

    def select_file_for_cell(self, item, column_index):
        """Open the existing validated picker directly from a file cell."""
        self.current_tree.selection_set(item)
        self.current_tree.focus(item)
        row_index = self.current_tree.index(item)
        rows = self.rows()
        if row_index >= len(rows):
            return "break"
        row = rows[row_index]
        material = str(row[0]).strip() if row else ""
        selected_path = select_crack_prop_file(
            self.winfo_toplevel(), material, column_index
        )
        if selected_path:
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            row[column_index] = selected_path
            self.app.mark_module_incomplete(self.module_name)
            values = list(row)
            values += [""] * max(0, len(self.column_headers) - len(values))
            self.current_tree.item(
                item, values=values[:len(self.column_headers)]
            )
            self.current_tree.update_idletasks()
            self.render_file_cell_overlay(item, column_index)
        return "break"

    def refresh_generated_paths(self, old_material_path=""):
        """Regenerate all rows after the configured Material Path changes."""
        material_path = (getattr(self.app, "settings_values", {}) or {}).get(
            "material_path", ""
        )
        for row in self.rows():
            row.extend([""] * max(0, len(self.column_headers) - len(row)))
            old_paths = build_crack_prop_file_paths(old_material_path, row)
            new_paths = build_crack_prop_file_paths(material_path, row)
            for old_path, path, (column_index, _, _) in zip(
                old_paths,
                new_paths,
                CRACK_PROP_FILE_COLUMNS,
            ):
                current = str(row[column_index]).strip()
                material = str(row[0]).strip() if row else ""
                is_auto_path = not current or current == FILE_NOT_FOUND or current == old_path
                if is_auto_path or validate_crack_prop_file(
                    current, material, column_index
                ) is not None:
                    row[column_index] = (
                        path
                        if path != FILE_NOT_FOUND
                        and file_path_colors(
                            path, material, column_index
                        )[0] == SUCCESS
                        else FILE_NOT_FOUND
                    )
        super().refresh_table()

    def validate_rows(self):
        result = super().validate_rows()
        missing_files = tuple(
            ValidationIssue(row_number, self.column_headers[column_index],
                            "file not found; select the file manually.")
            for row_number, row in enumerate(self.rows(), start=1)
            for column_index, _, _ in CRACK_PROP_FILE_COLUMNS
            if column_index < len(row)
            and (
                row[column_index] == FILE_NOT_FOUND
                or (
                    bool(str(row[column_index]).strip())
                    and (
                        not Path(str(row[column_index])).is_file()
                        or validate_crack_prop_file(
                            str(row[column_index]),
                            str(row[0]).strip() if row else "",
                            column_index,
                        ) is not None
                    )
                )
            )
        )
        if not missing_files:
            return result
        return ValidationResult(result.issues + missing_files)

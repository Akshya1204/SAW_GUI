"""Validated file selection and placement for Template Definition cells."""

import shutil
from pathlib import Path
from tkinter import filedialog, messagebox

from utils.template_definition_paths import (
    build_template_file_paths,
    validate_template_file,
    TEMPLATE_FILE_COLUMNS,
)


def select_template_file(parent, template_path, row_values, column_index):
    template = str(row_values[1] if len(row_values) > 1 else "").strip()
    invalid_template = (
        not template
        or template in {".", ".."}
        or any(character in template for character in '<>:"/\\|?*')
        or any(ord(character) < 32 for character in template)
        or template.endswith(".")
    )
    if invalid_template:
        messagebox.showerror(
            "Template Required",
            "Template is required before uploading a file.",
            parent=parent,
        )
        return None
    suffix = dict(TEMPLATE_FILE_COLUMNS).get(column_index)
    if suffix is None:
        return None
    selected = filedialog.askopenfilename(
        parent=parent,
        title="Select Template File",
        filetypes=[(f"Required file (*{suffix})", f"*{suffix}")],
    )
    if not selected:
        return None
    # Manual upload validation intentionally depends only on Template and cell.
    error = validate_template_file(selected, template, column_index)
    if error:
        messagebox.showerror("Invalid File", error, parent=parent)
        return None

    destination_paths = build_template_file_paths(template_path, row_values)
    position = [index for index, _ in TEMPLATE_FILE_COLUMNS].index(column_index)
    if destination_paths[position] == "Not Found":
        messagebox.showerror(
            "Upload Destination Unavailable",
            "The expected upload destination is unavailable. Complete Template Definition, Template Name, and Version first.",
            parent=parent,
        )
        return None
    destination = Path(destination_paths[position])
    source = Path(selected)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != destination.resolve():
            shutil.copy2(source, destination)
        if not destination.is_file():
            raise OSError("The selected file was not copied to the expected destination.")
    except OSError as error:
        messagebox.showerror("Upload Failed", str(error), parent=parent)
        return None
    return str(destination)

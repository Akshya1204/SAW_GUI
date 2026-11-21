"""Shared file picker for Crack Prop Material file cells."""

from pathlib import Path
from tkinter import filedialog, messagebox

from utils.crack_prop_paths import CRACK_PROP_FILE_TYPES, validate_crack_prop_file


def select_crack_prop_file(parent, material, column_index):
    """Pick and validate a file for one Crack Prop Material row cell."""
    rule = CRACK_PROP_FILE_TYPES.get(column_index)
    if rule is None:
        return None

    _, extension, label = rule
    material = str(material or "").strip()
    if not material:
        messagebox.showerror(
            "Material Required",
            "Enter the Material value in this row before selecting a file.",
            parent=parent,
        )
        return None

    selected_path = filedialog.askopenfilename(
        parent=parent,
        title=f"Select {label}",
        filetypes=[(f"{label} (*{extension})", f"*{extension}")],
    )
    if not selected_path:
        return None

    error = validate_crack_prop_file(
        selected_path, material, column_index
    )
    if error:
        messagebox.showerror("Invalid File", error, parent=parent)
        return None
    return str(Path(selected_path))

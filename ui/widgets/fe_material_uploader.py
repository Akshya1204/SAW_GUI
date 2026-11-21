"""File picker for Inelastic Material .item files."""

from pathlib import Path
from tkinter import filedialog, messagebox

from utils.fe_material_paths import validate_fe_item_file


def select_fe_item_file(parent, inelastic_code):
    code = str(inelastic_code or "").strip()
    if not code:
        messagebox.showerror(
            "Material Code Required",
            "Enter the Inelastic Material Code in this row before selecting a file.",
            parent=parent,
        )
        return None
    selected_path = filedialog.askopenfilename(
        parent=parent,
        title="Select Inelastic Material Item File",
        filetypes=[("Item files (*.item)", "*.item")],
    )
    if not selected_path:
        return None
    error = validate_fe_item_file(selected_path, code)
    if error:
        messagebox.showerror("Invalid File", error, parent=parent)
        return None
    return str(Path(selected_path))

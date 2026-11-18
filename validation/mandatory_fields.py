"""Creates Mandatory nd Optional fields, prompting the user the fill if anything is left out."""

import tkinter as tk
from tkinter import messagebox

MANDATORY_COLOR = "#B42318"
OPTIONAL_COLOR = "#667085"

def create_field_label(parent, description, required=False):
    """Create a field label with Mandatory/Optional text."""
    
    frame = tk.Frame(parent, bg="white")
    tk.Label(
        frame,
        text=description,
        font=("Arial", 9, "bold"),
        bg="white",
        fg="#253245"
    ).pack(side="left")
    
    tk.Label(
        frame,
        text=" * Mandatory" if required else " (Optional)",
        font=("Arial", 8),
        bg="white",
        fg=MANDATORY_COLOR if required else OPTIONAL_COLOR,
    ).pack(side="left")
    
    return frame

def is_missing(value):
    """Return True if a mandatory input is empty."""
    
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    
    return False

def validate_fields(field_definitions, values, parent=None):
    """Validate a dictionary of values against field definitions.

    Args:
        field_definitions (_type_): _description_
        values (_type_): _description_
        parent (_type_, optional): _description_. Defaults to None.
    """
    missing = []
    for field in field_definitions:
        if not field.get("required", False):
            continue
        
        name = field["name"]
        label = field.get(
            "description",
            field.get("label", name)
        )
        if is_missing(values.get(name)):
            missing.append(label)
            
    if missing:
        messagebox.showerror(
            "Mandatory Fields Missing",
            "Please fill the mandatory fields.\n\n"
            + "\n".join(missing),
            parent=parent,
        )
        return False
    return True

def validate_table_rows(field_definitions, rows, parent=None):
    """Validate multiple table records.
    Each row must be a dictionary keyed by field name.

    Args:
        field_definitions (_type_): _description_
        rows (_type_): _description_
        parent (_type_, optional): _description_. Defaults to None.
    """
    missing = []
    for row_number, row in enumerate(rows, start=1):
        for field in field_definitions:
            if not field.get("required", False):
                continue
            
            name = field["name"]
            
            if is_missing(row.get(name)):
                label = field.get(
                    "description",
                    field.get("label", name)
                )
                missing.append(
                    f"Row {row_number}: {label}"
                )
    if missing:
        messagebox.showerror(
            "Mandatory Fields Missing",
            "Please fill the mandatory fields.\n\n"
            + "\n".join(missing),
            parent=parent,
        )
        return False
    return True
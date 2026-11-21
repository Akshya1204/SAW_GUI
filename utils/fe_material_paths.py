"""Expected Inelastic Material item-file paths and validation."""

from pathlib import Path

from utils.constants import DANGER, SUCCESS
from utils.crack_prop_paths import FILE_NOT_FOUND

FE_ITEM_FILE_COLUMN = 4
FE_ITEM_TEXT_COLOR = "black"


def build_fe_item_file_path(material_path, row):
    """Build one FE Material row's expected Inelastic Material .item path."""
    if len(row) < 4:
        return FILE_NOT_FOUND
    code = str(row[1]).strip()
    version = str(row[2]).strip()
    rating = str(row[3]).strip()
    root = str(material_path or "").strip()
    if not all((root, code, version, rating)):
        return FILE_NOT_FOUND
    return str(Path(root) / rating / "FE_SC03" / code / version / f"{code}.item")


def validate_fe_item_file(file_path, inelastic_code):
    """Return an error unless path is exactly <current code>.item."""
    code = str(inelastic_code or "").strip()
    if not code:
        return "Enter the Inelastic Material Code in this row before selecting a file."
    expected = f"{code}.item"
    selected = Path(file_path)
    if selected.suffix != ".item" or selected.name != expected:
        return f"Select the file named {expected}."
    return None


def fe_item_file_colors(value, inelastic_code):
    """Return state colors without rechecking disk for a stored cell value."""
    valid = (
        str(value).strip() != FILE_NOT_FOUND
        and validate_fe_item_file(value, inelastic_code) is None
    )
    return (SUCCESS if valid else DANGER, FE_ITEM_TEXT_COLOR)

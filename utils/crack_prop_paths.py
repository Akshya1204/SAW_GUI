"""Expected Crack Prop Material file locations and status colors."""

from pathlib import Path

try:
    from utils.constants import DANGER, SUCCESS, WHITE
except ModuleNotFoundError as error:
    # Support `python utils/crack_prop_paths.py` as well as package imports.
    if error.name != "utils":
        raise
    from constants import DANGER, SUCCESS, WHITE


FILE_TEXT_COLOR = WHITE


CRACK_PROP_FILE_COLUMNS = (
    (4, "CP_Darwin", "_DAR.txt"),
    (5, "CP_Darwin", "_DAR_SK13.control"),
    (6, "CP_Darwin", "_SK13_Walker.csv"),
    (7, "CP_SA16", "_Paris_SA16.xlsx"),
    (8, "CP_SA16", "_Paris_SA16_SK13.xlsx"),
    (9, "CP_SA16", "_SK13_Walker.csv"),
)
FILE_NOT_FOUND = "Not found"
CRACK_PROP_FILE_TYPES = {
    4: ("_DAR.txt", ".txt", "DAR file"),
    5: ("_DAR_SK13.control", ".control", "SK13 control file"),
    6: ("_SK13_Walker.csv", ".csv", "SK13 Walker CSV"),
    7: ("_Paris_SA16.xlsx", ".xlsx", "SA16 Material file"),
    8: ("_Paris_SA16_SK13.xlsx", ".xlsx", "SA16SK13 control file"),
    9: ("_SK13_Walker.csv", ".csv", "SA16SK13 Walker CSV"),
}


def build_crack_prop_file_paths(material_path, row):
    """Build the six expected paths from one Crack Prop Material row."""
    if len(row) < 3:
        return (FILE_NOT_FOUND,) * len(CRACK_PROP_FILE_COLUMNS)

    material = str(row[0]).strip()
    version = str(row[1]).strip()
    export_rating = str(row[2]).strip()
    root = str(material_path or "").strip()
    if not all((root, material, version, export_rating)):
        return (FILE_NOT_FOUND,) * len(CRACK_PROP_FILE_COLUMNS)

    base = Path(root)
    return tuple(
        str(base / export_rating / folder / material / version / f"{material}{suffix}")
        for _, folder, suffix in CRACK_PROP_FILE_COLUMNS
    )


def file_path_colors(path, material=None, column_index=None):
    """Return colors when checking whether an expected file exists on disk."""
    valid = Path(path).is_file()
    if valid and column_index is not None:
        valid = validate_crack_prop_file(path, material, column_index) is None
    return (SUCCESS if valid else DANGER, FILE_TEXT_COLOR)


def file_state_colors(path, material=None, column_index=None):
    """Color an already stored file state without rechecking the filesystem."""
    valid = (
        str(path).strip() != FILE_NOT_FOUND
        and validate_crack_prop_file(path, material, column_index) is None
    )
    return (SUCCESS if valid else DANGER, FILE_TEXT_COLOR)


def validate_crack_prop_file(file_path, material, column_index):
    """Return an error when a selected path doesn't match its row and column."""
    rule = CRACK_PROP_FILE_TYPES.get(column_index)
    if rule is None:
        return "This cell is not a Crack Prop Material file column."
    suffix, extension, label = rule
    material = str(material or "").strip()
    if not material:
        return "Enter the Material value in this row before selecting a file."
    expected_filename = f"{material}{suffix}"
    selected = Path(file_path)
    if selected.suffix.lower() != extension:
        return f"Select a {extension} file for {label}."
    if selected.name != expected_filename:
        return f"Select the file named {expected_filename}."
    return None

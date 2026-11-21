"""Template Definition generated file paths and filename validation."""

from pathlib import Path

from utils.constants import DANGER, SUCCESS, WHITE

TEMPLATE_FILE_NOT_FOUND = "Not Found"
TEMPLATE_FILE_COLUMNS = (
    (3, ".json"),
    (4, ".pm"),
    (5, ".RFP"),
    (6, ".item"),
    (7, "_ELCOLOUR_0.item"),
    (8, "_UIF_0.uif"),
    (9, "_Slice_0.uif"),
    (10, "_SYMPLANES_0.item"),
)


def expected_template_filename(template_name, column_index):
    suffix = dict(TEMPLATE_FILE_COLUMNS).get(column_index)
    name = str(template_name or "").strip()
    return f"{name}{suffix}" if name and suffix else ""


def build_template_file_paths(template_path, row):
    """Build expected file paths for a Template Definition row."""
    if len(row) < 3:
        return (TEMPLATE_FILE_NOT_FOUND,) * len(TEMPLATE_FILE_COLUMNS)
    name, template, version = (str(value or "").strip() for value in row[:3])
    root = str(template_path or "").strip()
    if not all((root, name, template, version)):
        return (TEMPLATE_FILE_NOT_FOUND,) * len(TEMPLATE_FILE_COLUMNS)
    base = Path(root) / template / f"v{version}"
    return tuple(
        str(base / expected_template_filename(name, index))
        for index, _ in TEMPLATE_FILE_COLUMNS
    )


def validate_template_file(file_path, template_name, column_index):
    """Return an error unless the selected filename exactly matches its column."""
    expected = expected_template_filename(template_name, column_index)
    if not expected:
        return "Template Name is required before uploading a file."
    if Path(file_path).name != expected:
        return f"Select the file named {expected}."
    return None


def template_file_colors(value):
    valid = str(value).strip() != TEMPLATE_FILE_NOT_FOUND
    return (SUCCESS if valid else DANGER, WHITE)

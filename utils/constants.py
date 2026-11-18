"""Shared SAW application configuration and UI constants."""

APP_TITLE = "Specimen Analysis Workflow"

APP_SHORT_NAME = "SAW"

APP_VERSION = "0.6.5"

WINDOW_WIDTH = 1100

WINDOW_HEIGHT = 650

MIN_WIDTH = 820

MIN_HEIGHT = 520

FONT_FAMILY = "Segoe UI"

BACKGROUND = "#F3F5F7"

WHITE = "#FFFFFF"

TEXT = "#182630"

SECONDARY_TEXT = "#5F6D78"

MUTED_TEXT = "#8B97A1"

BORDER = "#D6DEE5"

PRIMARY = "#173D56"

PRIMARY_LIGHT = "#E8F0F4"

SUCCESS = "#2F6B55"

SUCCESS_LIGHT = "#E8F2ED"

STATUS_INCOMPLETE = "#B33F3F"

STATUS_INCOMPLETE_LIGHT = "#F8ECEC"

DISABLED_ACTION = "#B5C0C8"

HOVER_BG = "#F2F5F7"

NAV_ACTIVE = "#E8F0F4"

DARK_HEADER = "#0D1B29"

HEADER_MUTED = "#B7C3CC"

HEADER_VERSION = "#D7E0E6"

PRIMARY_HOVER = "#245873"

SECONDARY_ACCENT = "#607B88"

SECONDARY_ACCENT_LIGHT = "#ECF2F4"

PROGRESS_TRACK = "#DCE3E8"

SURFACE_MUTED = "#EFF3F5"

SURFACE_HOVER = "#E5EBEF"

DANGER = "#B33F3F"

DANGER_LIGHT = "#F8ECEC"

DANGER_HOVER = "#F4DCDC"

STATUS_WARNING_COLOR = "#A56600"

DIALOG_SUBTEXT = "#C6D1D9"

TABLE_HEADER = "#E8EFF3"

NAVIGATION_OPTIONS = [
            "Home",
    "Specimen Definition",
    "Template Definition",
    "FE Material",
    "Crack Prop Material",
    "Crack Geom Material",
    "Interpolation File Definition",
]

HAMBURGER_OPTIONS = [
    ("☷", "Instructions"),
    ("⚙", "Settings"),
    ("⎋", "Exit"),
]

COLUMN_HEADERS = [
    "Column 1", "Column 2", "Column 3", "Column 4", "Column 5",
    "Column 6", "Column 7", "Column 8", "Column 9"
]

YES_NO_OPTIONS = ("Yes", "No")

CRACK_DEFINITION_OPTIONS = (
    "None",
    "Single Crack",
    "Multiple Cracks",
)


MODULE_FIELD_DEFINITIONS = {
    "Specimen Definition": (
        {"label": "Specimen Name", "input_type": "Text Field"},
        {"label": "Template", "input_type": "Text Field"},
        {"label": "Material", "input_type": "Text Field"},
        {
            "label": "FE Material",
            "input_type": "File Picker",
            "picker_type": "file",
        },
        {
            "label": "Crack Definition",
            "input_type": "Dropdown",
            "options": CRACK_DEFINITION_OPTIONS,
        },
        {"label": "No of Crack Geoms", "input_type": "Number Field"},
        {"label": "No of Crack Material", "input_type": "Number Field"},
        {"label": "Temp (C)", "input_type": "Number Field"},
        {
            "label": "Stress (in MPa) or Strain (absolute)",
            "input_type": "Number Field",
        },
        {"label": "R-Ratio", "input_type": "Text Field"},
        {"label": "Ramp Up (s)", "input_type": "Number Field"},
        {"label": "Tensile Dwell (s)", "input_type": "Number Field"},
        {"label": "Ramp Down (s)", "input_type": "Number Field"},
        {"label": "Comp Dwell (s)", "input_type": "Number Field"},
        {"label": "Arkwright Cycle", "input_type": "Number Field"},
        {
            "label": "For Crack Prop (first cycle if blank)",
            "input_type": "Number Field",
        },
        {
            "label": "For Crack Prop (last cycle if blank)",
            "input_type": "Number Field",
        },
        {"label": "Creep Balance Type", "input_type": "Text Field"},
        {
            "label": "Elastic Model",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Arkwright Model",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Arkwright Post",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Run Darwin",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Run SK13",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Run SA16",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Run SK13 for SA16",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {
            "label": "Run Result Summary",
            "input_type": "Yes/No Dropdown",
            "options": YES_NO_OPTIONS,
        },
        {"label": "Life", "input_type": "Text Field"},
        {"label": "Depth", "input_type": "Text Field"},
    ),
    "Template Definition": (
        {"label": "Template Name", "input_type": "Text Field"},
        {"label": "Template", "input_type": "Text Field"},
        {"label": "Version", "input_type": "Text Field"},
        {
            "label": "JSON Template Settings File",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Template File",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Reference Point File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Arkwright Domain Item File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Elcolour Item File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Darwin Geometry UIF File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Darwin Slice UIF Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Darwin Symplanes Item File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
    ),
    "FE Material": (
        {"label": "Material", "input_type": "Text Field"},
        {"label": "Inelastic Material Code", "input_type": "Text Field"},
        {"label": "Material Version", "input_type": "Text Field"},
        {"label": "Export Control Rating", "input_type": "Text Field"},
        {
            "label": "Inelastic Material Item File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Elastic Material Item File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
    ),
    "Crack Prop Material": (
        {"label": "Material", "input_type": "Text Field"},
        {"label": "Crack Prop Version", "input_type": "Text Field"},
        {"label": "Export Control Rating", "input_type": "Text Field"},
        {
            "label": "Enabled",
            "input_type": "Dropdown",
            "options": ("Y", "N"),
            "required": True,
        },
        {"label": "DAR File", "input_type": "File Upload", "picker_type": "file"},
        {
            "label": "SK13 Control File",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "SK13 Walker CSV",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "SA16 Material File",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "SA16 SK13 Control File",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "SA16 SK13 Walker CSV",
            "input_type": "File Upload",
            "picker_type": "file",
        },
    ),
    "Crack Geom Material": (
        {"label": "Crack Def", "input_type": "Text Field"},
        {"label": "Crack Name", "input_type": "Text Field"},
        {"label": "Template Name", "input_type": "Text Field"},
        {"label": "DARWIN crack type", "input_type": "Text Field"},
        {"label": "w", "input_type": "Text Field"},
        {"label": "h", "input_type": "Text Field"},
        {"label": "crack_x", "input_type": "Text Field"},
        {"label": "crack_y", "input_type": "Text Field"},
        {"label": "w", "input_type": "Text Field"},
        {"label": "h", "input_type": "Text Field"},
        {"label": "crack_x", "input_type": "Text Field"},
        {"label": "crack_a", "input_type": "Text Field"},
        {"label": "crack_c", "input_type": "Text Field"},
    ),
    "Interpolation File Definition": (
        {"label": "Interpolation Name", "input_type": "Text Field"},
        {"label": "Interpolation Type", "input_type": "Text Field"},
        {"label": "Interpolation File Name", "input_type": "Text Field"},
        {"label": "Version", "input_type": "Text Field"},
        {"label": "Domains", "input_type": "Text Field"},
        {"label": "X", "input_type": "Text Field"},
        {"label": "Y", "input_type": "Text Field"},
        {"label": "Z", "input_type": "Text Field"},
        {"label": "Time", "input_type": "Text Field"},
        {"label": "Temp", "input_type": "Text Field"},
        {"label": "Max Rel Interpolation", "input_type": "Text Field"},
        {"label": "Stress All Time Points", "input_type": "Text Field"},
        {"label": "Interpolation Hardening", "input_type": "Text Field"},
        {
            "label": "Compress Interpolation Data",
            "input_type": "Text Field",
        },
        {
            "label": "Interpolation File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
        {
            "label": "Full File Path",
            "input_type": "File Upload",
            "picker_type": "file",
        },
    ),
}


MODULE_COLUMN_HEADERS = {
    module_name: [field["label"] for field in fields]
    for module_name, fields in MODULE_FIELD_DEFINITIONS.items()
}

MODULE_HEADER_GROUPS = {
    "Crack Geom Material": (
        {"label": "", "start": 0, "span": 3},
        {"label": "DARWIN", "start": 3, "span": 5},
        {"label": "SA16", "start": 8, "span": 3},
        {"label": "", "start": 11, "span": 2},
    ),
}

EDIT_HEADER = DARK_HEADER

EDIT_HEADER_ACCENT = "#2B6577"

EDIT_SURFACE = "#F6F8FA"

EDIT_GRID_HEADER = TABLE_HEADER

EDIT_GRID_ALT = "#F7F9FA"

EDIT_CELL_BORDER = "#C8D3DB"

EDIT_FOCUS = "#2C6F84"

ENTERPRISE_BLUE = "#173D56"

ENTERPRISE_BLUE_LIGHT = "#E8F0F4"

ENTERPRISE_BORDER = "#CDD7DF"

ENTERPRISE_TEXT = "#1F303C"

ENTERPRISE_MUTED = "#667784"

GROUP_HEADER = "#2B6577"

GROUP_HEADER_LIGHT = "#DDECEF"

GROUP_HEADER_EMPTY = "#EEF2F5"

CELL_BG = "#FFFFFF"

CELL_ALT_BG = "#F7F9FA"

CELL_BORDER = "#C8D3DB"

CELL_FOCUS_BORDER = "#2C6F84"

CELL_FOCUS_BG = "#F4FAFB"

CELL_PLACEHOLDER = "#91A0AA"

CELL_TEXT = "#22333F"

####
MANDATORY_MODULE_FIELDS = {
    "Specimen Definition": {
        "Specimen Name",
        "Template",
        "Material",
        "FE Material",
        "Crack Definition",
        "No of Crack Geoms",
        "No of Crack Material",
        "Temp (C)",
        "Stress (in MPa) or Strain (absolute)",
        "R-Ratio",
        "Ramp Up (s)",
        "Tensile Dwell (s)",
        "Ramp Down (s)",
        "Comp Dwell (s)",
        "Arkwright Cycle",
        "For Crack Prop (first cycle if blank)",
        "For Crack Prop (last cycle if blank)",
        "Creep Balance Type",
        "Elastic Model",
        "Arkwright Model",
        "Arkwright Post",
        "Run Darwin",
        "Run SK13",
        "Run SA16",
        "Run SK13 for SA16",
        "Run Result Summary",
        "Life",
        "Depth",
    },
    "Template Definition": {
        "Template Name",
        "Template",
        "Version",
        "JSON Template Settings File",
        "Template File",
        "Reference Point File Path",
        "Arkwright Domain Item File Path",
        "Elcolour Item File Path",
        "Darwin Geometry UIF File Path",
        "Darwin Slice UIF Path",
        "Darwin Symplanes Item File Path",
    },
    "FE Material": {
        "Material",
        "Inelastic Material Code",
        "Material Version",
        "Export Control Rating",
        "Inelastic Material Item File Path",
        "Elastic Material Item File Path",
    },
    "Crack Prop Material": {
        "Material",
        "Crack Prop Version",
        "Export Control Rating",
        "DAR File",
        "SK13 Control File",
        "SK13 Walker CSV",
        "SA16 Material File",
        "SA16 SK13 Control File",
        "SA16 SK13 Walker CSV",
    },
    "Crack Geom Material": {
        "Crack Def",
        "Crack Name",
        "Template Name",
        "DARWIN crack type",
        "w",
        "h",
        "crack_x",
        "crack_y",
        "w",
        "h",
        "crack_x",
        "crack_a",
        "crack_c",
    },
    "Interpolation File Definition": {
        "Interpolation Name",
        "Interpolation Type",
        "Interpolation File Name",
        "Version",
        "Domains",
        "X",
        "Y",
        "Z",
        "Temp",
        "Max Rel Interpolation",
        "Stress All Time Points",
        "Interpolation Hardening",
        "Compress Interpolation Data",
        "Interpolation File Path",
        "Full File Path",
    },
}

for _module_name, _fields in MODULE_FIELD_DEFINITIONS.items():
    for _field in _fields:
        _field.setdefault(
            "required",
            _field["label"] in MANDATORY_MODULE_FIELDS.get(
                _module_name, set()
            )
        )
"""Validation rules for the Crack Geom Material module."""

from validation.base import ModuleValidator
from validation.rules import choice, positive_number
from validation.types import FieldRule


CRACK_TYPE_OPTIONS = (
    "Edge Crack",
    "Center Crack",
    "Surface Crack",
    "Through Crack",
)


CRACK_GEOM_MATERIAL_VALIDATOR = ModuleValidator(
    (
        FieldRule("Crack ID"),
        FieldRule(
            "Crack Type",
            kind="choice",
            validator=choice(CRACK_TYPE_OPTIONS),
        ),
        FieldRule(
            "Crack Length",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule(
            "Crack Depth",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule("Crack Width", kind="positive number", validator=positive_number),
        FieldRule("Location"),
        FieldRule("Orientation"),
        FieldRule("Symmetry"),
        FieldRule("Notes"),
    )
)

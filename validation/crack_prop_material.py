"""Validation rules for the Crack Prop Material module."""

from validation.base import ModuleValidator
from validation.rules import choice, positive_number
from validation.types import FieldRule


LOAD_MODE_OPTIONS = ("Mode I", "Mode II", "Mixed Mode")


CRACK_PROP_MATERIAL_VALIDATOR = ModuleValidator(
    (
        FieldRule("Material ID"),
        FieldRule(
            "Load Mode",
            kind="choice",
            validator=choice(LOAD_MODE_OPTIONS),
        ),
        FieldRule("Paris C", kind="positive number", validator=positive_number),
        FieldRule("Paris m", kind="positive number", validator=positive_number),
        FieldRule(
            "Threshold Delta K",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule(
            "Critical Delta K",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule("Growth Law"),
        FieldRule("Unit System"),
        FieldRule("Notes"),
    )
)

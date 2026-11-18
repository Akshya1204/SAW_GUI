"""Validation rules for the Specimen Definition module."""

from validation.base import ModuleValidator
from validation.rules import choice, positive_number
from validation.types import FieldRule


SPECIMEN_TYPE_OPTIONS = (
    "Dog-bone",
    "Compact tension",
    "Cylindrical",
    "Custom",
)


SPECIMEN_DEFINITION_VALIDATOR = ModuleValidator(
    (
        FieldRule("Specimen ID"),
        FieldRule("Specimen Name"),
        FieldRule(
            "Specimen Type",
            kind="choice",
            validator=choice(SPECIMEN_TYPE_OPTIONS),
        ),
        FieldRule("Geometry"),
        FieldRule("Length", kind="positive number", validator=positive_number),
        FieldRule("Width", kind="positive number", validator=positive_number),
        FieldRule(
            "Thickness",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule("Orientation"),
        FieldRule("Notes"),
    )
)

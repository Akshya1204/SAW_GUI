"""Validation rules for the Interpolation File Definition module."""

from validation.base import ModuleValidator
from validation.rules import choice
from validation.types import FieldRule


INTERPOLATION_METHOD_OPTIONS = (
    "Linear",
    "Cubic Spline",
    "Nearest Neighbor",
    "PCHIP",
)


INTERPOLATION_FILE_VALIDATOR = ModuleValidator(
    (
        FieldRule("File ID"),
        FieldRule("File Name"),
        FieldRule("Data Type"),
        FieldRule("X Column"),
        FieldRule("Y Column"),
        FieldRule(
            "Interpolation Method",
            kind="choice",
            validator=choice(INTERPOLATION_METHOD_OPTIONS),
        ),
        FieldRule("Extrapolation"),
        FieldRule("Unit System"),
        FieldRule("Notes"),
    )
)

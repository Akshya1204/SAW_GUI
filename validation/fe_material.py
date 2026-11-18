"""Validation rules for the FE Material module."""

from validation.base import ModuleValidator
from validation.rules import choice, number, positive_number
from validation.types import FieldRule


UNIT_SYSTEM_OPTIONS = ("SI", "Imperial", "Custom")


FE_MATERIAL_VALIDATOR = ModuleValidator(
    (
        FieldRule("Material ID"),
        FieldRule("Material Name"),
        FieldRule(
            "Young's Modulus",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule("Poisson Ratio", kind="number", validator=number),
        FieldRule("Density", kind="positive number", validator=positive_number),
        FieldRule(
            "Yield Strength",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule(
            "Ultimate Strength",
            kind="positive number",
            validator=positive_number,
        ),
        FieldRule(
            "Unit System",
            kind="choice",
            validator=choice(UNIT_SYSTEM_OPTIONS),
        ),
        FieldRule("Notes"),
    )
)

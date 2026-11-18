"""Validation rules for the Template Definition module."""

from validation.base import ModuleValidator
from validation.rules import choice, positive_number
from validation.types import FieldRule


ANALYSIS_TYPE_OPTIONS = ("Static", "Fatigue", "Fracture", "Thermal")


TEMPLATE_DEFINITION_VALIDATOR = ModuleValidator(
    (
        FieldRule("Template ID"),
        FieldRule("Template Name"),
        FieldRule("Version"),
        FieldRule(
            "Analysis Type",
            kind="choice",
            validator=choice(ANALYSIS_TYPE_OPTIONS),
        ),
        FieldRule("Solver"),
        FieldRule("Mesh Size", kind="positive number", validator=positive_number),
        FieldRule("Unit System"),
        FieldRule("Author"),
        FieldRule("Notes"),
    )
)

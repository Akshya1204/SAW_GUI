"""Base validator that applies field rules to table rows."""

from typing import Iterable, List

from validation.rules import choice, number
from validation.types import FieldRule, ValidationIssue, ValidationResult


class ModuleValidator:
    def __init__(self, fields: Iterable[FieldRule]):
        self.fields = tuple(fields)

    def validate(self, rows: Iterable[Iterable[str]]) -> ValidationResult:
        rows = [list(row) for row in rows]
        if not rows:
            return ValidationResult(
                (
                    ValidationIssue(
                        None,
                        "Rows",
                        "add at least one row before submitting.",
                    ),
                )
            )

        issues: List[ValidationIssue] = []
        for row_number, row in enumerate(rows, start=1):
            for column_index, field in enumerate(self.fields):
                value = ""
                if column_index < len(row) and row[column_index] is not None:
                    value = str(row[column_index]).strip()

                if field.required and not value:
                    issues.append(
                        ValidationIssue(row_number, field.name, "is required.")
                    )
                    continue

                if value and field.validator:
                    error = field.validator(value)
                    if error:
                        issues.append(
                            ValidationIssue(row_number, field.name, error)
                        )

        return ValidationResult(tuple(issues))


def field_rules_from_definitions(field_definitions):
    """Build validation rules from the shared UI field definitions."""

    rules = []
    for field in field_definitions:
        input_type = field["input_type"]
        validator = None
        if input_type in ("Dropdown", "Yes/No Dropdown"):
            validator = choice(field.get("options", ()))
        elif input_type == "Number Field":
            validator = number
        rules.append(
            FieldRule(
                field["label"],
                kind=input_type,
                validator=validator,
            )
        )
    return tuple(rules)

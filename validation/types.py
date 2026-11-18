"""Shared types used by module-specific validators."""

from dataclasses import dataclass
from typing import Callable, Optional


FieldValidator = Callable[[str], Optional[str]]


@dataclass(frozen=True)
class FieldRule:
    """Validation metadata for one table column."""

    name: str
    kind: str = "text"
    required: bool = True
    validator: Optional[FieldValidator] = None


@dataclass(frozen=True)
class ValidationIssue:
    """A single validation problem that can be shown to the user."""

    row_number: Optional[int]
    field: str
    message: str

    def format(self) -> str:
        if self.row_number is None:
            return f"{self.field}: {self.message}"
        return f"Row {self.row_number} - {self.field}: {self.message}"


@dataclass(frozen=True)
class ValidationResult:
    """Validation outcome returned by every module validator."""

    issues: tuple[ValidationIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.issues

    def message(self, limit: int = 5) -> str:
        if self.is_valid:
            return ""

        visible_issues = list(self.issues[:limit])
        if len(self.issues) > limit:
            visible_issues.append(
                ValidationIssue(
                    None,
                    "Additional issues",
                    f"{len(self.issues) - limit} more issue(s) found.",
                )
            )

        return "Complete the fields below before submitting:\n\n" + "\n".join(
            issue.format() for issue in visible_issues
        )

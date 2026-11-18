"""Reusable field-level validation rules."""

import math
from typing import Iterable


def number(value: str):
    """Accept finite numeric input, including decimal and scientific notation."""

    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return "must be a valid number."

    if not math.isfinite(parsed):
        return "must be a finite number."
    return None


def positive_number(value: str):
    error = number(value)
    if error:
        return error
    if float(value) <= 0:
        return "must be greater than zero."
    return None


def choice(options: Iterable[str]):
    allowed = tuple(options)

    def validate(value: str):
        if value not in allowed:
            return "must be one of: " + ", ".join(allowed) + "."
        return None

    return validate

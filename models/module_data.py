"""Domain data structures for SAW module rows."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ModuleData:
    name: str
    rows: List[List[str]] = field(default_factory=list)

    def replace_rows(self, rows: List[List[str]]) -> None:
        self.rows = [list(row) for row in rows]

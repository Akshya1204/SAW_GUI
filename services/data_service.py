"""Data-access boundary for SAW.

The current application remains in-memory. This service is the intended
boundary for future Oracle/file persistence.
"""

from typing import Dict, List


class DataService:
    def __init__(self) -> None:
        self._data: Dict[str, List[List[str]]] = {}

    def get_rows(self, module_name: str) -> List[List[str]]:
        return [list(row) for row in self._data.get(module_name, [])]

    def replace_rows(self, module_name: str, rows: List[List[str]]) -> None:
        self._data[module_name] = [list(row) for row in rows]

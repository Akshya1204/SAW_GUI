"""Crack Geom Material workflow page."""

from ui.pages.module_page import ModulePage
from utils.constants import (
    MODULE_COLUMN_HEADERS,
    MODULE_FIELD_DEFINITIONS,
    MODULE_HEADER_GROUPS,
)


class CrackGeomMaterialPage(ModulePage):
    module_name = "Crack Geom Material"
    description = "Manage crack geometry material data."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]
    header_groups = MODULE_HEADER_GROUPS.get(module_name, ())

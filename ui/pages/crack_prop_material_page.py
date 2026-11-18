"""Crack Prop Material workflow page."""

from ui.pages.module_page import ModulePage
from utils.constants import MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS


class CrackPropMaterialPage(ModulePage):
    module_name = "Crack Prop Material"
    description = "Manage crack propagation material data."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

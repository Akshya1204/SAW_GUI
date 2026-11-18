"""FE Material workflow page."""

from ui.pages.module_page import ModulePage
from utils.constants import MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS


class FEMaterialPage(ModulePage):
    module_name = "FE Material"
    description = "Manage finite-element material information."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

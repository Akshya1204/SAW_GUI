"""Template Definition workflow page."""

from ui.pages.module_page import ModulePage
from utils.constants import MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS


class TemplateDefinitionPage(ModulePage):
    module_name = "Template Definition"
    description = "Manage template definition data."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

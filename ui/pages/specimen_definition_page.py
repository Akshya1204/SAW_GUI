"""Specimen Definition workflow page."""

from ui.pages.module_page import ModulePage
from utils.constants import MODULE_COLUMN_HEADERS, MODULE_FIELD_DEFINITIONS


class SpecimenDefinitionPage(ModulePage):
    module_name = "Specimen Definition"
    description = "Define and review specimen information."
    column_headers = MODULE_COLUMN_HEADERS[module_name]
    field_definitions = MODULE_FIELD_DEFINITIONS[module_name]

"""Registry mapping workflow modules to their validators."""

from utils.constants import MODULE_FIELD_DEFINITIONS
from validation.base import ModuleValidator, field_rules_from_definitions


VALIDATOR_REGISTRY = {
    module_name: ModuleValidator(field_rules_from_definitions(fields))
    for module_name, fields in MODULE_FIELD_DEFINITIONS.items()
}

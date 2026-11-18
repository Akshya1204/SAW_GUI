"""Page registry for the SAW workflow modules."""

import tkinter as tk
from typing import Callable, Dict

from ui.pages.crack_geom_material_page import CrackGeomMaterialPage
from ui.pages.crack_prop_material_page import CrackPropMaterialPage
from ui.pages.fe_material_page import FEMaterialPage
from ui.pages.interpolation_file_page import InterpolationFilePage
from ui.pages.specimen_definition_page import SpecimenDefinitionPage
from ui.pages.template_definition_page import TemplateDefinitionPage


PageFactory = Callable[[tk.Misc, object], tk.Frame]


PAGE_REGISTRY: Dict[str, PageFactory] = {
    "Specimen Definition": SpecimenDefinitionPage,
    "Template Definition": TemplateDefinitionPage,
    "FE Material": FEMaterialPage,
    "Crack Prop Material": CrackPropMaterialPage,
    "Crack Geom Material": CrackGeomMaterialPage,
    "Interpolation File Definition": InterpolationFilePage,
}

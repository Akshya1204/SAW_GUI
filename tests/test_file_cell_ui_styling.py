import unittest
from unittest.mock import patch

from utils.constants import DANGER, SUCCESS, WHITE
from utils.crack_prop_paths import FILE_NOT_FOUND
from utils.template_definition_paths import TEMPLATE_FILE_NOT_FOUND
from ui.pages.crack_prop_material_page import CrackPropMaterialPage
from ui.pages.fe_material_page import FEMaterialPage
from ui.pages.template_definition_page import TemplateDefinitionPage


class FakeLabel:
    def __init__(self, parent, **options):
        self.options = options
        self.placement = None
        self.bindings = {}

    def bind(self, event, callback):
        self.bindings[event] = callback

    def configure(self, **options):
        self.options.update(options)

    def winfo_exists(self):
        return True

    def place(self, **options):
        self.placement = options

    def place_forget(self):
        self.placement = None

    def lift(self):
        pass


class FakeTree:
    def __init__(self, values):
        self.values = tuple(values)

    def item(self, item, option):
        return {"values": self.values}[option]

    def bbox(self, item, column):
        return (10, 20, 240, 28)


class FileCellStyleTests(unittest.TestCase):
    def render(self, page_class, method_name, row, column, patch_target):
        page = type("PageHarness", (), {})()
        page.current_tree = FakeTree(row)
        page.column_ids = tuple(f"column_{index}" for index in range(len(row)))
        page._file_cell_labels = {}
        page._template_file_labels = {}
        with patch(patch_target, FakeLabel):
            if page_class is FEMaterialPage:
                getattr(page_class, method_name)(page, "row-1")
            elif method_name == "render_file_cell_overlay":
                getattr(page_class, method_name)(page, "row-1", column)
            else:
                getattr(page_class, method_name)(page, "row-1")
        labels = page._file_cell_labels or page._template_file_labels
        return labels[("row-1", column)]

    def assert_full_cell_state(self, label, value, background):
        self.assertEqual(label.options["text"], value)
        self.assertEqual(label.options["bg"], background)
        self.assertEqual(label.options["fg"], WHITE)
        self.assertEqual(label.placement, {"x": 10, "y": 20, "width": 240, "height": 28})

    def test_crack_prop_full_cell_red_and_green(self):
        missing = ["Akhil", "v1", "user", "Y", FILE_NOT_FOUND] + [""] * 5
        label = self.render(CrackPropMaterialPage, "render_file_cell_overlay", missing, 4,
                            "ui.pages.crack_prop_material_page.tk.Label")
        self.assert_full_cell_state(label, FILE_NOT_FOUND, DANGER)
        valid = list(missing)
        valid[4] = "C:/Akhil_DAR.txt"
        label = self.render(CrackPropMaterialPage, "render_file_cell_overlay", valid, 4,
                            "ui.pages.crack_prop_material_page.tk.Label")
        self.assert_full_cell_state(label, valid[4], SUCCESS)

    def test_fe_material_full_cell_red_and_green(self):
        missing = ["Material", "ABC123", "v1", "user", FILE_NOT_FOUND, ""]
        label = self.render(FEMaterialPage, "render_file_cell_overlay", missing, 4,
                            "ui.pages.fe_material_page.tk.Label")
        self.assert_full_cell_state(label, FILE_NOT_FOUND, DANGER)
        valid = list(missing)
        valid[4] = "C:/ABC123.item"
        label = self.render(FEMaterialPage, "render_file_cell_overlay", valid, 4,
                            "ui.pages.fe_material_page.tk.Label")
        self.assert_full_cell_state(label, valid[4], SUCCESS)

    def test_template_file_full_cell_red_and_green(self):
        missing = ["A", "T", "1", TEMPLATE_FILE_NOT_FOUND] + [""] * 7
        label = self.render(TemplateDefinitionPage, "render_file_cell_overlay", missing, 3,
                            "ui.pages.template_definition_page.tk.Label")
        self.assert_full_cell_state(label, TEMPLATE_FILE_NOT_FOUND, DANGER)
        valid = list(missing)
        valid[3] = "C:/A.json"
        label = self.render(TemplateDefinitionPage, "render_file_cell_overlay", valid, 3,
                            "ui.pages.template_definition_page.tk.Label")
        self.assert_full_cell_state(label, valid[3], SUCCESS)


if __name__ == "__main__":
    unittest.main()

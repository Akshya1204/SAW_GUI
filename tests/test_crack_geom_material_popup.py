import unittest

from ui.dialogs.edit_data_dialog import EditDataDialog
from ui.pages.crack_geom_material_page import CrackGeomMaterialPage
from utils.constants import MODULE_FIELD_DEFINITIONS, MODULE_HEADER_GROUPS


class CrackGeomMaterialLayoutTests(unittest.TestCase):
    def test_solver_groups_cover_the_existing_columns(self):
        fields = MODULE_FIELD_DEFINITIONS["Crack Geom Material"]
        labels = [field["label"] for field in fields]
        groups = MODULE_HEADER_GROUPS["Crack Geom Material"]

        darwin = groups[1]
        sa16 = groups[2]
        self.assertEqual(labels[darwin["start"]:darwin["start"] + darwin["span"]], [
            "DARWIN crack type", "w", "h", "crack_x", "crack_y",
        ])
        self.assertEqual(labels[sa16["start"]:sa16["start"] + sa16["span"]], [
            "w", "h", "crack_x",
        ])
        self.assertIs(CrackGeomMaterialPage.field_definitions, fields)

    def test_all_other_existing_headings_remain_in_order(self):
        labels = [
            field["label"]
            for field in MODULE_FIELD_DEFINITIONS["Crack Geom Material"]
        ]
        self.assertEqual(labels, [
            "Crack Def", "Crack Name", "Template Name", "DARWIN crack type",
            "w", "h", "crack_x", "crack_y", "w", "h", "crack_x",
            "crack_a", "crack_c",
        ])
        self.assertEqual(CrackGeomMaterialPage.header_groups, MODULE_HEADER_GROUPS[
            "Crack Geom Material"
        ])


class AddNewNumericValidationTests(unittest.TestCase):
    def setUp(self):
        self.dialog = object.__new__(EditDataDialog)

    def test_string_fields_are_not_numeric_validated(self):
        string_labels = {
            "Crack Def", "Crack Name", "Template Name", "DARWIN crack type",
        }
        fields = MODULE_FIELD_DEFINITIONS["Crack Geom Material"]
        self.assertEqual(
            {field["label"] for field in fields if field["label"] in string_labels},
            string_labels,
        )

    def test_numeric_fields_accept_integers_and_decimals_only(self):
        for value in ("10", "25", "10.5", "-5", "-10.25", ".5", "1e3"):
            with self.subTest(value=value):
                self.assertTrue(self.dialog.is_valid_numeric_value(value))
        for value in ("text", "1.2.3", "-", ".", "1e", "NaN", "Infinity"):
            with self.subTest(value=value):
                self.assertFalse(self.dialog.is_valid_numeric_value(value))


if __name__ == "__main__":
    unittest.main()

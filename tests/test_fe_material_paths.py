import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils.constants import DANGER, SUCCESS, WHITE
from utils.crack_prop_paths import FILE_NOT_FOUND
from utils.fe_material_paths import (
    build_fe_item_file_path,
    fe_item_file_colors,
    validate_fe_item_file,
)
from ui.dialogs.edit_data_dialog import EditDataDialog
from ui.pages.fe_material_page import FEMaterialPage


class FakeTree:
    def __init__(self, values):
        self.values = tuple(values)
        self.updates = 0

    def selection_set(self, item):
        pass

    def focus(self, item):
        pass

    def index(self, item):
        return 0

    def item(self, item, **options):
        if "values" in options:
            self.values = tuple(options["values"])
            self.updates += 1
        return {"values": self.values}

    def update_idletasks(self):
        pass


class FakeEntry:
    def __init__(self, value):
        self.value = value
        self.options = {}
        self._cell_frame = type("Frame", (), {"configure": lambda frame, **kw: None})()

    def get(self):
        return self.value

    def configure(self, **options):
        self.options.update(options)


class FEMaterialPathTests(unittest.TestCase):
    def test_expected_path_uses_each_row_values(self):
        one = build_fe_item_file_path("c:/demo", ["A", "ABC123", "v1", "user"])
        two = build_fe_item_file_path("d:/materials", ["B", "XYZ789", "v2", "restricted"])
        self.assertEqual(Path(one).as_posix(), "c:/demo/user/FE_SC03/ABC123/v1/ABC123.item")
        self.assertEqual(Path(two).as_posix(), "d:/materials/restricted/FE_SC03/XYZ789/v2/XYZ789.item")

    def test_missing_inputs_return_not_found(self):
        self.assertEqual(build_fe_item_file_path("", ["A", "ABC", "v1", "user"]), FILE_NOT_FOUND)
        self.assertEqual(build_fe_item_file_path("root", ["A", "", "v1", "user"]), FILE_NOT_FOUND)

    def test_exact_code_and_item_extension_required(self):
        self.assertIsNone(validate_fe_item_file("C:/files/ABC123.item", "ABC123"))
        for name in ("ABC123.txt", "ABC123.xlsx", "ABC123.csv", "ABC123_Item.item", "ABC123.item.txt", "XYZ123.item", "random.item"):
            with self.subTest(name=name):
                self.assertIsNotNone(validate_fe_item_file(name, "ABC123"))

    def test_cell_colors_are_red_or_green_with_white_text(self):
        self.assertEqual(fe_item_file_colors(FILE_NOT_FOUND, "ABC123"), (DANGER, WHITE))
        self.assertEqual(fe_item_file_colors("C:/missing/ABC123.item", "ABC123"), (SUCCESS, WHITE))

    def test_edit_dialog_missing_cell_is_centered_red_and_white(self):
        dialog = object.__new__(EditDataDialog)
        dialog.module_name = "FE Material"
        entries = [FakeEntry("Material"), FakeEntry("ABC123"), FakeEntry("v1"), FakeEntry("user"), FakeEntry(FILE_NOT_FOUND)]
        dialog.entries = [entries]
        entries[4]._row_index = 0
        entries[4]._column_index = 4
        dialog.set_fe_item_file_status(entries[4], FILE_NOT_FOUND)
        self.assertEqual(entries[4].options["bg"], DANGER)
        self.assertEqual(entries[4].options["fg"], WHITE)
        self.assertEqual(entries[4].options["justify"], "center")

    def test_dialog_populates_existing_expected_file_and_preserves_manual_path(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as root:
            values = ["Material", "ABC123", "v1", "user", FILE_NOT_FOUND]
            expected = Path(build_fe_item_file_path(root, values))
            expected.parent.mkdir(parents=True)
            expected.touch()
            dialog = object.__new__(EditDataDialog)
            dialog.module_name = "FE Material"
            dialog.material_path_getter = lambda: root
            entries = [FakeEntry(value) for value in values]
            dialog.entries = [entries]
            entries[4]._row_index = 0
            entries[4]._column_index = 4
            dialog.set_entry_value = lambda entry, value: setattr(entry, "value", value)
            EditDataDialog.regenerate_fe_material_row(dialog, entries)
            self.assertEqual(entries[4].get(), str(expected))
            manual = str(Path(root) / "selected" / "ABC123.item")
            entries[4].value = manual
            EditDataDialog.regenerate_fe_material_row(dialog, entries)
            self.assertEqual(entries[4].get(), manual)

    def test_main_table_uploader_updates_cell_and_cancel_preserves_it(self):
        selected = "C:/some/path/ABC123.item"
        row = ["Material", "ABC123", "v1", "user", FILE_NOT_FOUND, ""]
        rows = [row]
        tree = FakeTree(row)
        page = type("Harness", (), {})()
        page.current_tree = tree
        page.rows = lambda: rows
        page.column_headers = ["Material", "Code", "Version", "Rating", "Item", "Elastic"]
        page.module_name = "FE Material"
        page.app = type("App", (), {"mark_module_incomplete": lambda self, name: None})()
        page.winfo_toplevel = lambda: None
        page.render_file_cell_overlay = lambda item: None
        with patch("ui.pages.fe_material_page.select_fe_item_file", return_value=selected):
            FEMaterialPage.select_file_for_cell(page, "row-1")
        self.assertEqual(row[4], selected)
        self.assertEqual(tree.values[4], selected)
        with patch("ui.pages.fe_material_page.select_fe_item_file", return_value=None):
            FEMaterialPage.select_file_for_cell(page, "row-1")
        self.assertEqual(row[4], selected)
        self.assertEqual(tree.values[4], selected)


if __name__ == "__main__":
    unittest.main()

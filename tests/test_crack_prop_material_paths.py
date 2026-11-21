import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils.constants import DANGER, SUCCESS
from utils.crack_prop_paths import (
    CRACK_PROP_FILE_COLUMNS,
    FILE_TEXT_COLOR,
    FILE_NOT_FOUND,
    build_crack_prop_file_paths,
    file_path_colors,
    file_state_colors,
    validate_crack_prop_file,
)
from ui.dialogs.edit_data_dialog import EditDataDialog
from ui.pages.crack_prop_material_page import CrackPropMaterialPage


class FakeWidget:
    def __init__(self, value=""):
        self.options = {}
        self.value = value

    def configure(self, **options):
        self.options.update(options)

    def get(self):
        return self.value


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


class CrackPropMaterialPathTests(unittest.TestCase):
    def test_each_row_generates_all_six_paths_from_its_own_values(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as first_root, tempfile.TemporaryDirectory(dir=Path(__file__).parent) as second_root:
            first_row = ["Akhil", "clone", "user"]
            second_row = ["Boeing", "v2", "restricted"]

            first_paths = build_crack_prop_file_paths(first_root, first_row)
            second_paths = build_crack_prop_file_paths(second_root, second_row)

            self.assertEqual(len(first_paths), 6)
            self.assertEqual(len(second_paths), 6)
            self.assertEqual(
                [Path(path).relative_to(first_root).as_posix() for path in first_paths],
                [
                    "user/CP_Darwin/Akhil/clone/Akhil_DAR.txt",
                    "user/CP_Darwin/Akhil/clone/Akhil_DAR_SK13.control",
                    "user/CP_Darwin/Akhil/clone/Akhil_SK13_Walker.csv",
                    "user/CP_SA16/Akhil/clone/Akhil_Paris_SA16.xlsx",
                    "user/CP_SA16/Akhil/clone/Akhil_Paris_SA16_SK13.xlsx",
                    "user/CP_SA16/Akhil/clone/Akhil_SK13_Walker.csv",
                ],
            )
            self.assertEqual(
                [Path(path).relative_to(second_root).as_posix() for path in second_paths],
                [
                    "restricted/CP_Darwin/Boeing/v2/Boeing_DAR.txt",
                    "restricted/CP_Darwin/Boeing/v2/Boeing_DAR_SK13.control",
                    "restricted/CP_Darwin/Boeing/v2/Boeing_SK13_Walker.csv",
                    "restricted/CP_SA16/Boeing/v2/Boeing_Paris_SA16.xlsx",
                    "restricted/CP_SA16/Boeing/v2/Boeing_Paris_SA16_SK13.xlsx",
                    "restricted/CP_SA16/Boeing/v2/Boeing_SK13_Walker.csv",
                ],
            )

    def test_incomplete_row_or_settings_path_shows_not_found(self):
        self.assertEqual(
            build_crack_prop_file_paths("", ["A", "v1", "user"]),
            (FILE_NOT_FOUND,) * 6,
        )
        self.assertEqual(
            build_crack_prop_file_paths("root", ["A", "", "user"]),
            (FILE_NOT_FOUND,) * 6,
        )
        self.assertEqual(file_path_colors(FILE_NOT_FOUND), (DANGER, FILE_TEXT_COLOR))

    def test_file_status_colors_follow_file_existence(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            file_path = Path(directory) / "selected.dat"
            self.assertEqual(file_path_colors(file_path), (DANGER, FILE_TEXT_COLOR))
            file_path.touch()
            self.assertEqual(file_path_colors(file_path), (SUCCESS, FILE_TEXT_COLOR))

    def test_existing_but_wrong_material_file_stays_red(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            wrong_material = Path(directory) / "Boeing_DAR.txt"
            wrong_material.touch()
            self.assertEqual(
                file_path_colors(wrong_material, "Akhil", 4),
                (DANGER, FILE_TEXT_COLOR),
            )

    def test_stored_valid_path_state_stays_green_without_disk_recheck(self):
        selected_path = Path("C:/selected/Akhil_DAR.txt")
        self.assertFalse(selected_path.is_file())
        self.assertEqual(
            file_state_colors(selected_path, "Akhil", 4),
            (SUCCESS, FILE_TEXT_COLOR),
        )
        self.assertEqual(
            file_state_colors(FILE_NOT_FOUND, "Akhil", 4),
            (DANGER, FILE_TEXT_COLOR),
        )

    def test_valid_uploader_selection_updates_model_and_visible_row_immediately(self):
        row = ["Akhil", "clone", "user", "Y"] + [FILE_NOT_FOUND] * 6
        rows = [row]
        tree = FakeTree(row)
        rendered = []
        page = type("PageHarness", (), {})()
        page.current_tree = tree
        page.rows = lambda: rows
        page.column_headers = [str(index) for index in range(10)]
        page.module_name = "Crack Prop Material"
        page.app = type("AppHarness", (), {
            "mark_module_incomplete": lambda self, name: None,
        })()
        page.winfo_toplevel = lambda: None
        page.render_file_cell_overlay = lambda item, column: rendered.append(
            (item, column)
        )

        selected_path = "C:/demo/Akhil_DAR.txt"
        with patch(
            "ui.pages.crack_prop_material_page.select_crack_prop_file",
            return_value=selected_path,
        ):
            CrackPropMaterialPage.select_file_for_cell(page, "row-1", 4)

        self.assertEqual(row[4], selected_path)
        self.assertEqual(tree.values[4], selected_path)
        self.assertEqual(tree.updates, 1)
        self.assertEqual(rendered, [("row-1", 4)])

    def test_cancelled_or_invalid_picker_keeps_cell_value_and_state(self):
        selected_path = "C:/demo/Akhil_DAR.txt"
        row = ["Akhil", "clone", "user", "Y", selected_path] + ["x"] * 5
        rows = [row]
        tree = FakeTree(row)
        page = type("PageHarness", (), {})()
        page.current_tree = tree
        page.rows = lambda: rows
        page.column_headers = [str(index) for index in range(10)]
        page.module_name = "Crack Prop Material"
        page.app = type("AppHarness", (), {
            "mark_module_incomplete": lambda self, name: None,
        })()
        page.winfo_toplevel = lambda: None
        page.render_file_cell_overlay = lambda item, column: None

        for picker_result in (None, None):
            with patch(
                "ui.pages.crack_prop_material_page.select_crack_prop_file",
                return_value=picker_result,
            ):
                CrackPropMaterialPage.select_file_for_cell(page, "row-1", 4)
            self.assertEqual(row[4], selected_path)
            self.assertEqual(tree.values[4], selected_path)
            self.assertEqual(tree.updates, 0)

    def test_existing_uploader_status_uses_green_and_missing_uses_red(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            existing = Path(directory) / "Akhil_DAR.txt"
            for path, expected_background, create_file, justification in (
                (FILE_NOT_FOUND, DANGER, False, "center"),
                (str(existing), SUCCESS, True, "left"),
            ):
                if create_file:
                    existing.touch()
                entry = FakeWidget()
                entry._cell_frame = FakeWidget()
                entry._row_index = 0
                entry._column_index = 4
                material = FakeWidget("Akhil")
                dialog = object.__new__(EditDataDialog)
                dialog.entries = [[material]]
                EditDataDialog.set_file_path_status(
                    dialog, entry, str(path)
                )
                self.assertEqual(entry.options["bg"], expected_background)
                self.assertEqual(entry.options["fg"], FILE_TEXT_COLOR)
                self.assertEqual(entry._cell_frame.options["bg"], expected_background)
                self.assertEqual(entry.options["justify"], justification)

    def test_not_found_status_is_centered(self):
        entry = FakeWidget()
        entry._cell_frame = FakeWidget()
        EditDataDialog.set_file_path_status(
            object.__new__(EditDataDialog), entry, FILE_NOT_FOUND
        )
        self.assertEqual(entry.options["justify"], "center")

    def test_column_mapping_covers_the_six_existing_upload_fields(self):
        self.assertEqual(
            [column for column, _, _ in CRACK_PROP_FILE_COLUMNS],
            [4, 5, 6, 7, 8, 9],
        )

    def test_each_column_validates_extension_and_exact_material_filename(self):
        expected = {
            4: ("Akhil_DAR.txt", ".txt"),
            5: ("Akhil_DAR_SK13.control", ".control"),
            6: ("Akhil_SK13_Walker.csv", ".csv"),
            7: ("Akhil_Paris_SA16.xlsx", ".xlsx"),
            8: ("Akhil_Paris_SA16_SK13.xlsx", ".xlsx"),
            9: ("Akhil_SK13_Walker.csv", ".csv"),
        }
        for column, (filename, _) in expected.items():
            with self.subTest(column=column):
                self.assertIsNone(
                    validate_crack_prop_file(filename, "Akhil", column)
                )
                self.assertIsNotNone(
                    validate_crack_prop_file("Boeing" + filename[5:], "Akhil", column)
                )
                wrong_extension = str(Path(filename).with_suffix(".wrong"))
                self.assertIsNotNone(
                    validate_crack_prop_file(wrong_extension, "Akhil", column)
                )

    def test_same_filename_rule_uses_each_rows_material(self):
        self.assertIsNone(
            validate_crack_prop_file("Boeing_DAR.txt", "Boeing", 4)
        )
        self.assertIsNotNone(
            validate_crack_prop_file("Akhil_DAR.txt", "Boeing", 4)
        )
        self.assertIsNotNone(
            validate_crack_prop_file("random.txt", "Akhil", 4)
        )

    def test_dar_requires_exact_uppercase_suffix(self):
        self.assertIsNone(
            validate_crack_prop_file("Akhil_DAR.txt", "Akhil", 4)
        )
        for filename in ("Akhil_Dar.txt", "Akhil_DAR.csv", "Akhil_DAR.xlsx"):
            with self.subTest(filename=filename):
                self.assertIsNotNone(
                    validate_crack_prop_file(filename, "Akhil", 4)
                )


if __name__ == "__main__":
    unittest.main()

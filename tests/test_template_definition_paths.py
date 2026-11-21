import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils.template_definition_paths import (
    TEMPLATE_FILE_COLUMNS,
    TEMPLATE_FILE_NOT_FOUND,
    build_template_file_paths,
    template_file_colors,
    validate_template_file,
)
from utils.constants import DANGER, SUCCESS, WHITE
from ui.pages.template_definition_page import TemplateDefinitionPage
from ui.widgets.template_file_uploader import select_template_file
from utils.crack_prop_paths import FILE_TEXT_COLOR
from utils.fe_material_paths import FE_ITEM_TEXT_COLOR


class TemplateDefinitionPathTests(unittest.TestCase):
    def test_all_eight_expected_paths_use_current_row(self):
        paths = build_template_file_paths("c:/user", ["LC_PLAIN", "LC_PLAIN", "1"])
        self.assertEqual([Path(path).as_posix() for path in paths], [
            "c:/user/LC_PLAIN/v1/LC_PLAIN.json",
            "c:/user/LC_PLAIN/v1/LC_PLAIN.pm",
            "c:/user/LC_PLAIN/v1/LC_PLAIN.RFP",
            "c:/user/LC_PLAIN/v1/LC_PLAIN.item",
            "c:/user/LC_PLAIN/v1/LC_PLAIN_ELCOLOUR_0.item",
            "c:/user/LC_PLAIN/v1/LC_PLAIN_UIF_0.uif",
            "c:/user/LC_PLAIN/v1/LC_PLAIN_Slice_0.uif",
            "c:/user/LC_PLAIN/v1/LC_PLAIN_SYMPLANES_0.item",
        ])
        other = build_template_file_paths("d:/templates", ["AIRFRAME", "CUSTOM", "2"])
        self.assertIn("AIRFRAME.json", other[0])
        self.assertIn("CUSTOM/v2", other[0].replace("\\", "/"))

    def test_incomplete_sources_do_not_generate_partial_path(self):
        for root, row in (("", ["A", "T", "1"]), ("root", ["", "T", "1"]), ("root", ["A", "", "1"]), ("root", ["A", "T", ""])):
            self.assertEqual(build_template_file_paths(root, row), (TEMPLATE_FILE_NOT_FOUND,) * 8)

    def test_exact_filename_is_required_for_each_column(self):
        expected = [
            "A.json", "A.pm", "A.RFP", "A.item", "A_ELCOLOUR_0.item",
            "A_UIF_0.uif", "A_Slice_0.uif", "A_SYMPLANES_0.item",
        ]
        for (column, _), filename in zip(TEMPLATE_FILE_COLUMNS, expected):
            with self.subTest(column=column):
                self.assertIsNone(validate_template_file(filename, "A", column))
                self.assertIsNotNone(validate_template_file("wrong.txt", "A", column))
        self.assertIsNotNone(validate_template_file("A.json", "", 3))

    def test_status_colors_and_darwin_group(self):
        self.assertEqual(template_file_colors(TEMPLATE_FILE_NOT_FOUND), (DANGER, WHITE))
        self.assertEqual(template_file_colors("/tmp/A.json"), (SUCCESS, WHITE))
        self.assertEqual(FILE_TEXT_COLOR, WHITE)
        self.assertEqual(FE_ITEM_TEXT_COLOR, WHITE)
        page_groups = TemplateDefinitionPage.header_groups
        self.assertEqual(page_groups[-1], {"label": "Darwin Template Files (3D ONLY)", "start": 8, "span": 3})

    def test_uploader_rejects_wrong_filename_and_copies_valid_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            root = Path(temp) / "library"
            source = Path(temp) / "LC_PLAIN.json"
            source.write_text("{}", encoding="utf-8")
            # Template drives manual filename validation; Template Name still
            # determines the unchanged generated upload destination.
            row = ["DIFFERENT_NAME", "LC_PLAIN", "1"]
            with patch("ui.widgets.template_file_uploader.filedialog.askopenfilename", return_value=str(source)):
                result = select_template_file(None, str(root), row, 3)
            expected = root / "LC_PLAIN" / "v1" / "DIFFERENT_NAME.json"
            self.assertEqual(Path(result), expected)
            self.assertEqual(expected.read_text(encoding="utf-8"), "{}")

            wrong = Path(temp) / "other.json"
            wrong.write_text("{}", encoding="utf-8")
            with patch("ui.widgets.template_file_uploader.filedialog.askopenfilename", return_value=str(wrong)), patch("ui.widgets.template_file_uploader.messagebox.showerror") as error:
                self.assertIsNone(select_template_file(None, str(root), row, 3))
                error.assert_called_once()

    def test_template_is_required_before_picker_opens(self):
        with patch("ui.widgets.template_file_uploader.filedialog.askopenfilename") as picker, patch("ui.widgets.template_file_uploader.messagebox.showerror") as error:
            self.assertIsNone(select_template_file("parent", "root", ["NAME", "", "1"], 3))
            picker.assert_not_called()
            self.assertIn("Template is required", error.call_args.args[1])

    def test_manual_filename_validation_uses_template_not_template_name(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            source = Path(temp) / "LC_PLAIN.json"
            source.write_text("{}", encoding="utf-8")
            row = ["DIFFERENT_NAME", "LC_PLAIN", "5"]
            with patch("ui.widgets.template_file_uploader.filedialog.askopenfilename", return_value=str(source)):
                selected = select_template_file(None, temp, row, 3)
            self.assertEqual(Path(selected).name, "DIFFERENT_NAME.json")

            wrong = Path(temp) / "LC_PLAIN_TEST.json"
            wrong.write_text("{}", encoding="utf-8")
            with patch("ui.widgets.template_file_uploader.filedialog.askopenfilename", return_value=str(wrong)), patch("ui.widgets.template_file_uploader.messagebox.showerror") as error:
                self.assertIsNone(select_template_file(None, temp, row, 3))
                error.assert_called_once()

    def test_each_upload_cell_validates_filename_from_template_value(self):
        filenames = (
            "TEMPLATE.json", "TEMPLATE.pm", "TEMPLATE.RFP", "TEMPLATE.item",
            "TEMPLATE_ELCOLOUR_0.item", "TEMPLATE_UIF_0.uif",
            "TEMPLATE_Slice_0.uif", "TEMPLATE_SYMPLANES_0.item",
        )
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            row = ["OTHER_NAME", "TEMPLATE", "1"]
            for (column, _), filename in zip(TEMPLATE_FILE_COLUMNS, filenames):
                source = Path(temp) / filename
                source.write_text("ok", encoding="utf-8")
                with self.subTest(column=column), patch(
                    "ui.widgets.template_file_uploader.filedialog.askopenfilename",
                    return_value=str(source),
                ):
                    result = select_template_file(None, temp, row, column)
                    self.assertEqual(Path(result).name, "OTHER_NAME" + filename[len("TEMPLATE"):])

                wrong_extension = source.with_suffix(".wrong")
                wrong_extension.write_text("bad", encoding="utf-8")
                with self.subTest(column=column, wrong_extension=True), patch(
                    "ui.widgets.template_file_uploader.filedialog.askopenfilename",
                    return_value=str(wrong_extension),
                ), patch("ui.widgets.template_file_uploader.messagebox.showerror") as error:
                    self.assertIsNone(select_template_file(None, temp, row, column))
                    error.assert_called_once()


if __name__ == "__main__":
    unittest.main()

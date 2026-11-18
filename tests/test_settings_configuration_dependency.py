import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from ui.dialogs.configuration_dialog import CONFIGURATION_FIELDS
from ui.pages.settings_page import BASIC_SETTINGS, SettingsPage


class FakeEntry:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class BasicSettingsDependencyTests(unittest.TestCase):
    def make_settings(self, paths):
        settings = SimpleNamespace(
            settings_fields={key: FakeEntry(value) for key, value in paths.items()}
        )
        settings.get_basic_path_values = lambda: SettingsPage.get_basic_path_values(settings)
        return settings

    def test_required_configuration_options_are_preserved(self):
        self.assertEqual(
            [field["key"] for field in CONFIGURATION_FIELDS],
            [
                "darwin_folder", "darwin_key", "darwin_path", "sc03_path",
                "sk13_path", "sk13_gen", "sk19_folder", "sk19_gen",
            ],
        )
        self.assertTrue(all(field.get("required") for field in CONFIGURATION_FIELDS))

    def test_all_valid_existing_paths_enable_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            python = root / "python.exe"
            python.touch()
            saw = root / "saw"
            saw.mkdir()
            (saw / "run_saw.py").touch()
            folders = []
            for name in ("material", "template", "work", "output"):
                folder = root / name
                folder.mkdir()
                folders.append(str(folder))
            values = [str(python), str(saw), *folders]
            settings = self.make_settings(
                {field["name"]: value for field, value in zip(
                    (field for field in BASIC_SETTINGS if field.get("required")),
                    values,
                )}
            )

            self.assertEqual(SettingsPage.validate_basic_paths(settings), [])

    def test_empty_or_invalid_required_path_blocks_configuration(self):
        settings = self.make_settings(
            {field["name"]: "" for field in BASIC_SETTINGS if field.get("required")}
        )
        self.assertEqual(len(SettingsPage.validate_basic_paths(settings)), 6)
        settings.settings_fields["path_to_python_executable"] = FakeEntry("missing.exe")
        self.assertTrue(SettingsPage.validate_basic_paths(settings))


if __name__ == "__main__":
    unittest.main()

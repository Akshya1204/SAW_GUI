# SAW Settings consolidation and required-field audit

## Mandatory/Optional audit

- `utils/constants.py`: corrected 12 mismatched labels in `MANDATORY_MODULE_FIELDS` so their required status matches the real field definitions. Previously these were silently treated as optional (e.g. `Run DARWIN` vs `Run Darwin`, `sk13 Control File` vs `SK13 Control File`, `Reference Point FIle Path` typo).
- `ui/dialogs/edit_data_dialog.py`: existing required/optional header indicators and Save checks verified in all six modules. Partially completed rows trigger the Missing Mandatory Fields warning.
- `ui/pages/module_page.py`: existing Submit validation retained.
- `ui/pages/settings_page.py`: existing required/optional indicators and Apply checks retained; typo in warning title corrected. Existing saved values now populate form controls when reopening; Apply updates existing settings instead of overwriting configuration keys.
- `ui/dialogs/configuration_dialog.py`: existing required/optional indicators and Save checks retained. Fixed broken variable reference in Save's entry collection (`entry` vs `value`).

## Combined Settings window

- Menu Settings now opens one two-tab window (Application Settings, SAW Configuration).
- `SettingsPage` and the configuration form are reused in separate `ttk.Notebook` tabs, including their independent scrollable forms, browse/check/validate controls and buttons.
- Home > SAW Configuration opens the second tab of that same Settings window, instead of creating another Toplevel.
- Configuration Save no longer closes the whole shared window; Configuration Cancel switches back to Application Settings.
- Both pages retain their independent required-field checks and save their values into `app.settings_values`.

## Verification performed

- Python bytecode compilation of all modules passed.
- Headless Tkinter smoke tests passed: combined window creation, two tabs, menu/home tab routing, required-field warnings and save logic, persistence across page saves, and dialog creation and incomplete-row checks for all six workflow modules.
- Full engineering workflow and actual browse/check integrations require testing with external SAW tools and paths on your Windows environment.

## Classification caveat

The ZIP supplied by the user already marked nearly all module fields as required. After fixing label mismatches, the counts are Specimen 28/28, Template 11/11, FE Material 6/6, Crack Prop Material 9/9, Crack Geom Material 13/13, Interpolation File 15/16. Configuration also marks all ten configuration fields as required. These were preserved as the user's existing selections and should be reviewed against engineering requirements.

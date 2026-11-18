# SAW — Modular v1

## Run

From this directory:

```bash
python main.py
```

## Architecture

- `main.py` — executable entry point
- `app/` — application composition and lifecycle
- `ui/pages/` — Home, Settings, Instructions, and module-specific pages
- `ui/dialogs/` — reusable data-entry dialogs
- `validation/` — shared validation engine, field rules, and module validators
- `ui/` — shared application shell and navigation
- `modules/` — module/domain definitions
- `models/` — data models
- `services/` — data-access boundary
- `utils/` — shared constants/configuration

Each workflow page owns its own title, description, column headers, dropdown
field, and future page-specific behavior. Shared table and edit behavior lives
in reusable page/dialog components. The current application still uses
in-memory data; the service layer remains ready for future Oracle/file
persistence without coupling database code to Tkinter widgets.

Validation runs when a workflow page is submitted. Each module has its own
validator in `validation/`, and each field can define a separate rule such as
text, choice, numeric, file, folder, or a custom cross-field check. The shared
page only displays the validation result and manages completion state.

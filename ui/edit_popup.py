"""Reusable EditPopupMixin UI/application mixin."""

import tkinter as tk
from tkinter import ttk, messagebox
from utils.constants import *

class EditPopupMixin:
    def open_add_new_popup(self):
        self.open_edit_popup(mode="new")


    def open_edit_popup(self, mode="update"):
        if not self.current_module:
            return

        if mode == "update" and not self.module_data.get(self.current_module, []):
            messagebox.showwarning(
                "No Existing Data",
                "There are no existing records to update. Use Add New first.",
                parent=self.root,
            )
            return

        module_headers = MODULE_COLUMN_HEADERS.get(
            self.current_module, COLUMN_HEADERS
        )
        dialog_title = (
            "Add New Data" if mode == "new" else "Update Existing Data"
        )

        # Do not open duplicate edit windows.
        existing = self.child_windows.get("edit")
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_force()
            return

        self.edit_record_label = None
        self.edit_status_label = None
        self.edit_mode = mode
        self.set_progress(25)

        window = tk.Toplevel(self.root)
        self.child_windows["edit"] = window

        window.title(f"SAW | {dialog_title} - {self.current_module}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        edit_width = min(1200, max(760, screen_width - 80))
        edit_height = min(680, max(480, screen_height - 120))
        window.geometry(f"{edit_width}x{edit_height}")
        window.minsize(
            min(900, edit_width),
            min(500, edit_height),
        )
        window.configure(bg=BACKGROUND)

        # Use a normal desktop window so the operating system provides
        # minimize, maximize/restore, resize, and close controls.
        window.resizable(True, True)
        window.overrideredirect(False)
        try:
            window.wm_attributes("-toolwindow", False)
        except tk.TclError:
            pass

        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_edit_popup(window)
        )

        self.center_window(window)

        # Open in a large desktop-friendly state. The title-bar
        # maximize/minimize buttons remain available to the user.
        window.update_idletasks()

        # Polished popup header.
        header = tk.Frame(window, bg=ENTERPRISE_BLUE, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_block = tk.Frame(header, bg=EDIT_HEADER)
        title_block.pack(side="left", fill="y", padx=18)

        tk.Label(
            title_block,
            text=dialog_title,
            font=(FONT_FAMILY, 14, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
        ).pack(anchor="w", pady=(11, 0))

        tk.Label(
            title_block,
            text=self.current_module,
            font=(FONT_FAMILY, 8),
            fg=DIALOG_SUBTEXT,
            bg=ENTERPRISE_BLUE,
        ).pack(anchor="w")

        tk.Label(
            header,
            text=f"{len(module_headers)} COLUMNS",
            font=(FONT_FAMILY, 8, "bold"),
            fg=WHITE,
            bg=EDIT_HEADER_ACCENT,
            padx=10,
            pady=5,
        ).pack(side="right", padx=18, pady=18)

        # Instruction strip.
        instruction = tk.Frame(
            window,
            bg=ENTERPRISE_BLUE_LIGHT,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        instruction.pack(fill="x", padx=18, pady=(12, 10))

        tk.Label(
            instruction,
            text="✎",
            font=(FONT_FAMILY, 12, "bold"),
            fg=ENTERPRISE_BLUE,
            bg=ENTERPRISE_BLUE_LIGHT,
        ).pack(side="left", padx=(12, 7), pady=8)

        tk.Label(
            instruction,
            text=(
                "Enter data directly in the cells. "
                "Use '+ Add Row' to add additional records."
            ),
            font=(FONT_FAMILY, 9),
            fg=ENTERPRISE_TEXT,
            bg=ENTERPRISE_BLUE_LIGHT,
        ).pack(side="left", pady=8)

        body = tk.Frame(window, bg=BACKGROUND)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        # Excel-like grid.
        grid_outer = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
            bd=0,
            padx=1,
            pady=1,
        )
        grid_outer.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 10),
        )

        canvas = tk.Canvas(
            grid_outer,
            bg=WHITE,
            highlightthickness=0,
        )

        vertical_scroll = ttk.Scrollbar(
            grid_outer,
            orient="vertical",
            command=canvas.yview,
        )

        horizontal_scroll = ttk.Scrollbar(
            grid_outer,
            orient="horizontal",
            command=canvas.xview,
        )

        canvas.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        grid_outer.grid_rowconfigure(0, weight=1)
        grid_outer.grid_columnconfigure(0, weight=1)

        grid = tk.Frame(canvas, bg=WHITE)
        canvas_window = canvas.create_window(
            (0, 0), window=grid, anchor="nw"
        )

        grid.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            ),
        )

        canvas.bind(
            "<Configure>",
            lambda event: self.resize_edit_grid_canvas(
                canvas, canvas_window, event
            ),
        )

        # Header row with an Excel-style row-number column.
        corner_frame = tk.Frame(
            grid,
            padx=5,
            pady=1,
            bg=CELL_BORDER,
        )
        corner_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 1),
            pady=(0, 1),
        )

        tk.Label(
            corner_frame,
            text="#",
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=TABLE_HEADER,
            width=5,
            padx=5,
            pady=7,
        ).pack(fill="both", expand=True)

        for column_index, header_text in enumerate(module_headers):
            header_frame = tk.Frame(
                grid,
                bg=CELL_BORDER,
                padx=1,
                pady=1,
            )
            header_frame.grid(
                row=0,
                column=column_index + 1,
                sticky="nsew",
                padx=1,
                pady=(0, 1),
            )

            tk.Label(
                header_frame,
                text=header_text,
                font=(FONT_FAMILY, 9, "bold"),
                fg=ENTERPRISE_TEXT,
                bg=TABLE_HEADER,
                width=16,
                anchor="w",
                padx=8,
                pady=7,
                cursor="arrow",
            ).pack(fill="both", expand=True)

        for column_index in range(len(module_headers) + 1):
            grid.grid_columnconfigure(column_index, weight=1)

        entries = []
        row_labels = []

        existing_rows = (
            self.module_data.get(self.current_module, [])
            if mode == "update"
            else []
        )
        if existing_rows:
            for row in existing_rows:
                self.add_edit_row(grid, entries, row, row_labels)
        else:
            self.add_edit_row(grid, entries, row_labels=row_labels)

        # Enterprise action/status bar.
        controls = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=ENTERPRISE_BORDER,
            highlightthickness=1,
        )
        controls.grid(row=1, column=0, sticky="ew", ipady=8)
        controls.grid_columnconfigure(1, weight=1)

        left_controls = tk.Frame(controls, bg=WHITE)
        left_controls.grid(row=0, column=0, sticky="w", padx=10)

        tk.Button(
            left_controls,
            text="+  Add Row",
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_BLUE,
            bg=ENTERPRISE_BLUE_LIGHT,
            activebackground=PRIMARY_LIGHT,
            activeforeground=ENTERPRISE_BLUE,
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=lambda: self.add_edit_row(
                grid, entries, row_labels=row_labels
            ),
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            left_controls,
            text="−  Delete Row",
            font=(FONT_FAMILY, 9, "bold"),
            fg=DANGER,
            bg=DANGER_LIGHT,
            activebackground=DANGER_HOVER,
            activeforeground=DANGER,
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=lambda: self.delete_selected_edit_row(
                entries, row_labels
            ),
        ).pack(side="left")

        status_controls = tk.Frame(controls, bg=WHITE)
        status_controls.grid(row=0, column=1, sticky="w", padx=12)

        self.edit_record_label = tk.Label(
            status_controls,
            text=f"Records: {len(entries)}",
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=WHITE,
        )
        self.edit_record_label.pack(side="left")

        self.edit_status_label = tk.Label(
            status_controls,
            text="Ready for data entry",
            font=(FONT_FAMILY, 8),
            fg=ENTERPRISE_MUTED,
            bg=WHITE,
        )
        self.edit_status_label.pack(side="left", padx=(12, 0))

        right_controls = tk.Frame(controls, bg=WHITE)
        right_controls.grid(row=0, column=2, sticky="e", padx=10)

        tk.Button(
            right_controls,
            text="Cancel",
            font=(FONT_FAMILY, 9, "bold"),
            fg=ENTERPRISE_TEXT,
            bg=SURFACE_MUTED,
            activebackground=SURFACE_HOVER,
            relief="flat",
            bd=0,
            padx=18,
            pady=7,
            cursor="hand2",
            command=lambda: self.close_edit_popup(window),
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            right_controls,
            text="OK  ✓",
            font=(FONT_FAMILY, 9, "bold"),
            fg=WHITE,
            bg=ENTERPRISE_BLUE,
            activebackground=PRIMARY_HOVER,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=22,
            pady=7,
            cursor="hand2",
            command=lambda: self.apply_edit_rows(
                window, entries, mode
            ),
        ).pack(side="left")

        # Focus first cell.
        if entries and entries[0]:
            entries[0][0].focus_set()


    def safe_configure_edit_label(self, label_name, **options):
        label = getattr(self, label_name, None)
        if label is None:
            return

        try:
            if label.winfo_exists():
                label.configure(**options)
        except tk.TclError:
            setattr(self, label_name, None)


    def add_edit_row(
        self, grid, entries, values=None, row_labels=None
    ):
        if row_labels is None:
            row_labels = []

        row_number = len(entries) + 1
        values = list(values) if values else []
        module_headers = MODULE_COLUMN_HEADERS.get(
            self.current_module, COLUMN_HEADERS
        )
        values += [""] * max(0, len(module_headers) - len(values))

        row_entries = []
        row_bg = CELL_ALT_BG if row_number % 2 == 0 else CELL_BG

        number_label = tk.Label(
            grid,
            text=str(row_number),
            font=(FONT_FAMILY, 8, "bold"),
            fg=ENTERPRISE_MUTED,
            bg=row_bg,
            width=5,
            relief="flat",
            bd=0,
            padx=5,
            pady=6,
        )
        number_label.grid(
            row=row_number,
            column=0,
            sticky="nsew",
            padx=(0, 1),
            pady=1,
        )

        for column_index in range(len(module_headers)):
            cell_frame = tk.Frame(
                grid,
                bg=CELL_BORDER,
                padx=1,
                pady=1,
            )
            cell_frame.grid(
                row=row_number,
                column=column_index + 1,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            entry = tk.Entry(
                cell_frame,
                font=(FONT_FAMILY, 9),
                fg=CELL_TEXT,
                bg=row_bg,
                relief="flat",
                bd=0,
                width=18,
                insertbackground=CELL_FOCUS_BORDER,
                insertwidth=2,
                highlightthickness=0,
                justify="left",
            )
            entry.pack(
                fill="both",
                expand=True,
                ipady=6,
                padx=3,
            )

            value = values[column_index]
            if value:
                entry.insert(0, value)

            entry._cell_frame = cell_frame
            entry._placeholder = ""

            entry.bind(
                "<FocusIn>",
                lambda event, widget=entry:
                self.cell_focus_in(widget),
                add="+",
            )
            entry.bind(
                "<FocusOut>",
                lambda event, widget=entry, bg=row_bg:
                self.cell_focus_out(widget, bg),
                add="+",
            )
            entry.bind(
                "<Return>",
                lambda event, widget=entry:
                self.focus_next_edit_cell(widget, entries),
            )

            row_entries.append(entry)

        entries.append(row_entries)
        row_labels.append(number_label)

        self.safe_configure_edit_label(
            "edit_record_label",
            text=f"Records: {len(entries)}",
        )
        self.safe_configure_edit_label(
            "edit_status_label",
            text="New row added - enter the required values",
        )

        row_entries[0].focus_set()


    def cell_focus_in(self, widget):
        frame = getattr(widget, "_cell_frame", None)
        if frame is not None:
            frame.configure(
                bg=CELL_FOCUS_BORDER,
                padx=2,
                pady=2,
            )

        if widget._placeholder and widget.get() == widget._placeholder:
            widget.delete(0, "end")
            widget.configure(fg=CELL_TEXT)

        widget.configure(bg=CELL_FOCUS_BG)


    def cell_focus_out(self, widget, original_bg):
        frame = getattr(widget, "_cell_frame", None)
        if frame is not None:
            frame.configure(
                bg=CELL_BORDER,
                padx=1,
                pady=1,
            )

        if not widget.get().strip():
            widget.delete(0, "end")
            widget.configure(
                fg=CELL_TEXT,
                bg=original_bg,
            )
        else:
            widget.configure(
                fg=CELL_TEXT,
                bg=original_bg,
            )


    def focus_next_edit_cell(self, widget, entries):
        for row_index, row in enumerate(entries):
            for col_index, cell in enumerate(row):
                if cell is widget:
                    if col_index + 1 < len(row):
                        row[col_index + 1].focus_set()
                    elif row_index + 1 < len(entries):
                        entries[row_index + 1][0].focus_set()
                    return "break"


    def delete_selected_edit_row(self, entries, row_labels):
        focused_widget = self.root.focus_get()

        selected_row = None
        for index, row in enumerate(entries):
            if focused_widget in row:
                selected_row = index
                break

        if selected_row is None:
            if not entries:
                return
            selected_row = len(entries) - 1

        for widget in entries[selected_row]:
            cell_frame = getattr(widget, "_cell_frame", None)
            if cell_frame is not None:
                cell_frame.destroy()
            else:
                widget.destroy()

        row_labels[selected_row].destroy()

        del entries[selected_row]
        del row_labels[selected_row]

        for index, row in enumerate(entries):
            new_row = index + 1
            row_labels[index].configure(text=str(new_row))
            row_labels[index].grid_configure(row=new_row)

            row_bg = CELL_ALT_BG if new_row % 2 == 0 else CELL_BG

            for widget in row:
                frame = getattr(widget, "_cell_frame", None)
                if frame is not None:
                    frame.grid_configure(row=new_row)
                    frame.configure(bg=CELL_BORDER)
                widget.configure(bg=row_bg)

        self.safe_configure_edit_label(
            "edit_record_label",
            text=f"Records: {len(entries)}",
        )
        self.safe_configure_edit_label(
            "edit_status_label",
            text="Selected row removed",
        )

        if entries:
            entries[min(selected_row, len(entries) - 1)][0].focus_set()


    def resize_edit_grid_canvas(self, canvas, canvas_window, event):
        # Keep the grid at least as wide as the available canvas while
        # still allowing horizontal scrolling for the nine columns.
        grid = canvas.nametowidget(
            canvas.itemcget(canvas_window, "window")
        )
        requested_width = grid.winfo_reqwidth()
        canvas.itemconfigure(
            canvas_window,
            width=max(event.width, requested_width)
        )


    def apply_edit_rows(self, window, entries, mode="update"):
        rows = []

        for row_entries in entries:
            values = [("" if entry.get().strip() == entry._placeholder else entry.get().strip()) for entry in row_entries]

            # Ignore completely empty rows.
            if any(values):
                rows.append(values)

        if not rows:
            messagebox.showwarning(
                "No Data",
                "Please enter at least one row of data.",
                parent=window,
            )
            return

        if mode == "new":
            existing_rows = self.module_data.get(self.current_module, [])
            self.module_data[self.current_module] = [
                list(row) for row in existing_rows
            ] + rows
        else:
            self.module_data[self.current_module] = rows
        self.refresh_main_table()

        self.set_progress(75)
        self.close_edit_popup(window)


    def close_edit_popup(self, window):
        if window.winfo_exists():
            try:
                window.grab_release()
            except tk.TclError:
                pass
            window.destroy()

        self.child_windows.pop("edit", None)
        self.edit_record_label = None
        self.edit_status_label = None
        self.edit_mode = None


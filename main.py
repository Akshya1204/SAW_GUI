"""SAW application entry point."""

import tkinter as tk

from app.application import SAWApplication


def main() -> None:
    root = tk.Tk()
    SAWApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

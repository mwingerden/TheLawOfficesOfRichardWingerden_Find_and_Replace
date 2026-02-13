import os
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askdirectory

class GUI:
    def __init__(self):
        self._root = tk.Tk()
        self._frame = tk.Frame(self._root)

    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()

    def _set_up_gui(self):
        self._root.title("Find And Replace")

        self._frame.pack(padx=10, pady=10, fill="x", expand=True)

        source_folder_frame = tk.Frame(self._frame)
        source_folder_frame.pack(fill="x", padx=5, pady=5)
        self._source_entry = tk.Entry(source_folder_frame, width=100)
        self._source_entry.grid(row=0, column=0)
        self._source_btn = tk.Button(
            source_folder_frame,
            text="Find Source Folder",
            command=lambda: self._find_folder(self._source_entry)
        )
        self._source_btn.grid(row=0, column=1, padx=5, pady=5)

    def _find_folder(self, entry_widget):
        path = askdirectory()

        if not path:
            self._source_folder = None
            entry_widget.config(state=NORMAL)
            entry_widget.delete(0, tk.END)
            entry_widget.config(state=DISABLED)
            return

        folder_name = os.path.basename(path)
        parent_folder = os.path.basename(os.path.dirname(path))

        entry_widget.config(state=NORMAL)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, f".../{parent_folder}/{folder_name}")
        entry_widget.config(state=DISABLED)

        self._source_folder = path
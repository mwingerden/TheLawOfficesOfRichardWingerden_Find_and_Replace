import os
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askdirectory

class GUI:
    def __init__(self):
        self._root = tk.Tk()
        self._frame = tk.Frame(self._root)
        self._find_replace_list = []
        self._find_replace_row = 1

    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()

    def _set_up_gui(self):
        self._root.title("Find And Replace")

        self._frame.pack(padx=10, pady=10, fill="x", expand=True)

        self._find_folder_gui(self._frame)

        self._find_replace_gui(self._frame)

        self._add_find_replace_button_gui(self._frame)

    def _find_folder_gui(self, frame):
        _source_folder_frame = tk.Frame(frame)
        _source_folder_frame.pack(fill="x", padx=5, pady=5)
        _source_entry = tk.Entry(_source_folder_frame, width=100)
        _source_entry.grid(row=0, column=0)
        _source_btn = tk.Button(
            _source_folder_frame,
            text="Find Source Folder",
            command=lambda: self._find_folder(_source_entry)
        )
        _source_btn.grid(row=0, column=1, padx=5, pady=5)

    def _find_replace_gui(self, frame):
        self._find_replace_frame = tk.Frame(frame)
        self._find_replace_frame.pack(fill="x", padx=5, pady=5)

        _find_what_label = tk.Label(
            self._find_replace_frame,
            text="Find What?"
        )
        _replace_with_label = tk.Label(
            self._find_replace_frame,
            text="Replace With?"
        )

        _find_what_label.grid(row=0, column=0, padx=5, pady=5)
        _replace_with_label.grid(row=0, column=1, padx=5, pady=5)

        self._find_what_variable = tk.StringVar()
        self._find_what_entry = tk.Entry(
            self._find_replace_frame,
            width=30,
            textvariable=self._find_what_variable,
        )
        self._replace_with_variable = tk.StringVar()
        self._replace_with_entry = tk.Entry(
            self._find_replace_frame,
            width=30,
            textvariable=self._replace_with_variable,
        )

        self._find_what_entry.grid(row=self._find_replace_row, column=0, padx=5, pady=5)
        self._replace_with_entry.grid(row=self._find_replace_row, column=1, padx=5, pady=5)

    def _add_find_replace_button_gui(self, frame):
        _add_frame = tk.Frame(frame)
        _add_frame.pack(fill="x", padx=5, pady=5)
        _add_btn = tk.Button(_add_frame,
                             text="Add New Find And Replace Instruction",
                             command=lambda: self._add_find_replace_instruction_gui())
        _add_btn.grid(row=0, column=0, padx=5, pady=5)

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

    def _add_find_replace_instruction_gui(self):
        if not self._find_what_variable.get().strip():
            messagebox.showerror("Warning",
                                 "Enter in text for what you want to find.")
            return

        if not self._replace_with_variable.get().strip():
            messagebox.showerror("Warning",
                                 "Enter in text for what you want to replace.")
            return

        if self._find_what_variable.get() != "" and self._replace_with_variable.get() != "":
            temp = (self._find_what_variable.get(), self._replace_with_variable.get())
            if temp not in self._find_replace_list:
                self._find_replace_list.append(temp)
            else:
                messagebox.showinfo("Duplicate Entry",
                                     "You entered " + temp[0] + " and " + temp[1] + "\nThey are already in the list.")

        self._add_new_find_replace_row_gui()

    def _add_new_find_replace_row_gui(self):
        find_text = self._find_what_variable.get().strip()
        replace_text = self._replace_with_variable.get().strip()

        # Create labels
        find_label = tk.Label(
            self._find_replace_frame,
            text=find_text
        )
        replace_label = tk.Label(
            self._find_replace_frame,
            text=replace_text
        )

        # Create remove button
        remove_btn = tk.Button(
            self._find_replace_frame,
            text="Remove",
            command=lambda: self._remove_row(find_label, replace_label, remove_btn, (find_text, replace_text))
        )

        # Place them
        find_label.grid(row=self._find_replace_row, column=0, padx=5, pady=5)
        replace_label.grid(row=self._find_replace_row, column=1, padx=5, pady=5)
        remove_btn.grid(row=self._find_replace_row, column=2, padx=5, pady=5)

        # Move entry widgets down
        self._find_replace_row += 1
        self._find_what_entry.grid(row=self._find_replace_row, column=0, padx=5, pady=5)
        self._replace_with_entry.grid(row=self._find_replace_row, column=1, padx=5, pady=5)

        # Clear inputs
        self._find_what_variable.set("")
        self._replace_with_variable.set("")

    def _remove_row(self, find_label, replace_label, remove_btn, value_tuple):
        # Remove from internal data list
        if value_tuple in self._find_replace_list:
            self._find_replace_list.remove(value_tuple)

        # Destroy widgets
        find_label.destroy()
        replace_label.destroy()
        remove_btn.destroy()
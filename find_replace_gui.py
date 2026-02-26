import os
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askdirectory

from find_and_replace import FindAndReplace


class FindReplaceGUI:

    def __init__(self):
        self._root = tk.Tk()
        self._frame = tk.Frame(self._root)

        self._source_folder = None
        self._find_replace_list = []
        self._find_replace_row = 1

        self._find_replace_frame = None
        self._find_what_variable = tk.StringVar()
        self._replace_with_variable = tk.StringVar()

        self._find_what_entry = None
        self._replace_with_entry = None

        self._find_replace_engine = FindAndReplace()
        self._reports = []

    def run(self):
        self._setup_gui()
        self._root.mainloop()

    def _setup_gui(self):
        self._root.title("Find and Replace")

        self._frame.pack(padx=10, pady=10, fill="x", expand=True)

        self._create_folder_section(self._frame)
        self._create_find_replace_section(self._frame)
        self._create_add_button(self._frame)
        self._create_execute_button(self._frame)

    def _create_folder_section(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        entry = tk.Entry(frame, width=100)
        entry.grid(row=0, column=0)

        button = tk.Button(
            frame,
            text="Select Source Folder",
            command=lambda: self._select_folder(entry),
        )
        button.grid(row=0, column=1, padx=5, pady=5)

    def _create_find_replace_section(self, parent):
        self._find_replace_frame = tk.Frame(parent)
        self._find_replace_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            self._find_replace_frame,
            text="Find What?",
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(
            self._find_replace_frame,
            text="Replace With?",
        ).grid(row=0, column=1, padx=5, pady=5)

        self._find_what_entry = tk.Entry(
            self._find_replace_frame,
            width=30,
            textvariable=self._find_what_variable,
        )

        self._replace_with_entry = tk.Entry(
            self._find_replace_frame,
            width=30,
            textvariable=self._replace_with_variable,
        )

        self._find_what_entry.grid(row=1, column=0, padx=5, pady=5)
        self._replace_with_entry.grid(row=1, column=1, padx=5, pady=5)

    def _create_add_button(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        button = tk.Button(
            frame,
            text="Add Find and Replace Instruction",
            command=self._add_instruction,
        )
        button.grid(row=0, column=0, padx=5, pady=5)

    def _create_execute_button(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        button = tk.Button(
            frame,
            text="Start Find and Replace",
            command=self._execute,
        )
        button.pack(padx=5, pady=5)

    def _select_folder(self, entry_widget):
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

    def _add_instruction(self):
        find_text = self._find_what_variable.get().strip()
        replace_text = self._replace_with_variable.get().strip()

        if not find_text:
            messagebox.showerror("Warning", "Enter text for what you want to find.")
            return

        if not replace_text:
            messagebox.showerror("Warning", "Enter text for what you want to replace.")
            return

        instruction = (find_text, replace_text)

        if instruction in self._find_replace_list:
            messagebox.showinfo(
                "Duplicate Entry",
                f"You entered '{find_text}' and '{replace_text}'.\n"
                "They are already in the list.",
            )
            return

        self._find_replace_list.append(instruction)
        self._add_instruction_row(find_text, replace_text)

        self._find_what_variable.set("")
        self._replace_with_variable.set("")

    def _add_instruction_row(self, find_text, replace_text):
        find_label = tk.Label(self._find_replace_frame, text=find_text)
        replace_label = tk.Label(self._find_replace_frame, text=replace_text)

        remove_button = tk.Button(
            self._find_replace_frame,
            text="Remove",
            command=lambda: self._remove_row(
                find_label, replace_label, remove_button, (find_text, replace_text)
            ),
        )

        find_label.grid(row=self._find_replace_row, column=0, padx=5, pady=5)
        replace_label.grid(row=self._find_replace_row, column=1, padx=5, pady=5)
        remove_button.grid(row=self._find_replace_row, column=2, padx=5, pady=5)

        self._find_replace_row += 1

        self._find_what_entry.grid(row=self._find_replace_row, column=0, padx=5, pady=5)
        self._replace_with_entry.grid(row=self._find_replace_row, column=1, padx=5, pady=5)

    def _remove_row(self, find_label, replace_label, remove_button, instruction):
        if instruction in self._find_replace_list:
            self._find_replace_list.remove(instruction)

        find_label.destroy()
        replace_label.destroy()
        remove_button.destroy()

    def _execute(self):
        if not self._find_replace_list:
            messagebox.showerror("Warning", "You didn't enter any instructions.")
            return

        if not self._source_folder:
            messagebox.showerror("Warning", "You didn't enter a folder.")
            return

        for find_text, replace_text in self._find_replace_list:
            self._reports.append(self._find_replace_engine.find_and_replace(self._source_folder,
                                                                            find_text,
                                                                            replace_text))

        for report in self._reports:
            if not report.success:
                messagebox.showerror("Error", report.message)
            else:
                messagebox.showinfo(
                    "Complete",
                    f"Processed {report.files_processed} files.\n"
                    f"Modified {report.files_modified} files.\n"
                    f"Total replacements: {report.total_replacements}"
                )
        self._reports.clear()

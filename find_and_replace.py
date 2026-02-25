import logging
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FindReplaceReport:
    success: bool
    files_processed: int = 0
    total_replacements: int = 0
    files_modified: int = 0
    warnings: list[str] = field(default_factory=list)
    error_message: str | None = None


class FindAndReplace:

    def __init__(self):
        self._source_folder: Path | None = None
        self._word_find: str | None = None
        self._word_replace: str | None = None
        self._list_word_doc_files: list[Path] = []
        self._file_order = [
            "Portfolio Inserts",
            "Fiduciary and Distribution Summary",
            "Trust Quick Reference Page",
            "Trust Summary",
            "RLT",
            "Pour-Over Will",
            "Funding Instructions",
            "Power of Attorney",
            "California Certification of Trust",
            "Assignment of Personal Property",
            "California Advance Health Care Directive",
            "California HIPAA Authorization",
            "California Nomination of Conservator",
            "Remembrance and Services Memorandum",
            "Personal Property Memo",
            "California Nomination of Guardian"
        ]

    def find_and_replace(self, source_folder: str, word_find: str, word_replace: str) -> FindReplaceReport:
        self._source_folder = Path(source_folder)
        self._word_find = word_find
        self._word_replace = word_replace
        report = FindReplaceReport(success=False)

        if not self._verify_folder():
            report.error_message = f"Folder not found: {self._source_folder}"
            return report

        if not self._find_docx_files():
            report.error_message = "No .docx files found."
            return report

        if not word_find:
            raise ValueError("word_find must not be blank")

        if not word_replace:
            raise ValueError("word_replace must not be blank")

        print(self._list_word_doc_files)
        report.success = True
        return report

    def _verify_folder(self):
        if not self._source_folder.is_dir():
            logging.warning("Folder not found: %s", self._source_folder)
            return False
        return True

    def _find_docx_files(self) -> bool:
        self._list_word_doc_files = [
            file
            for file in self._source_folder.iterdir()
            if file.suffix.lower() == ".docx"
               and file.name.startswith(tuple(self._file_order))
               and file.is_file()
        ]

        if not self._list_word_doc_files:
            logging.warning("No matching .docx files found.")
            return False

        return True

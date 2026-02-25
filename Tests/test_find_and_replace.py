import pytest

from find_and_replace import FindAndReplace

@pytest.fixture
def service(tmp_path):
    """Create a FindAndReplace instance with a temporary folder."""
    f = FindAndReplace()
    f._source_folder = tmp_path
    return f

def test_find_and_replace_folder_not_found(tmp_path):
    service = FindAndReplace()
    non_existent = tmp_path / "does_not_exist"

    report = service.find_and_replace(non_existent, "find", "replace")

    assert report.success is False
    assert "Folder not found" in report.error_message


def test_find_and_replace_no_docx_files(tmp_path):
    service = FindAndReplace()

    # Create folder but no matching docx files
    (tmp_path / "random.txt").touch()

    report = service.find_and_replace(tmp_path, "find", "replace")

    assert report.success is False
    assert report.error_message == "No .docx files found."


def test_find_and_replace_blank_word_find(tmp_path):
    service = FindAndReplace()

    # Create matching docx file so it passes earlier checks
    (tmp_path / "Portfolio Inserts Example.docx").touch()

    with pytest.raises(ValueError):
        service.find_and_replace(tmp_path, "", "replace")


def test_find_and_replace_blank_word_replace(tmp_path):
    service = FindAndReplace()

    (tmp_path / "Portfolio Inserts Example.docx").touch()

    with pytest.raises(ValueError):
        service.find_and_replace(tmp_path, "find", "")


def test_find_and_replace_success(tmp_path):
    service = FindAndReplace()

    (tmp_path / "Portfolio Inserts Example.docx").touch()

    report = service.find_and_replace(tmp_path, "find", "replace")

    assert report.success is True

def test_verify_folder_exists(tmp_path):
    # tmp_path is a temporary folder that exists
    service = FindAndReplace()
    service._source_folder = tmp_path

    result = service._verify_folder()
    assert result is True

def test_verify_folder_does_not_exist(tmp_path):
    # Create a path that does NOT exist
    non_existent = tmp_path / "nonexistent"
    service = FindAndReplace()
    service._source_folder = non_existent

    result = service._verify_folder()
    assert result is False


def test_find_docx_files_found(service, tmp_path):
    # Create files that match _file_order
    file1 = tmp_path / "Portfolio Inserts Example.docx"
    file1.touch()
    file2 = tmp_path / "Trust Summary Notes.docx"
    file2.touch()

    # Also create a file that shouldn't match
    other_file = tmp_path / "Random.docx"
    other_file.touch()

    result = service._find_docx_files()

    # Should return True since at least one file matches _file_order
    assert result is True

    # _list_word_doc_files should only include matching files
    filenames = [f.name for f in service._list_word_doc_files]
    assert "Portfolio Inserts Example.docx" in filenames
    assert "Trust Summary Notes.docx" in filenames
    assert "Random.docx" not in filenames


def test_find_docx_files_none_found(service, tmp_path):
    # Create files that do NOT match _file_order
    (tmp_path / "Random.docx").touch()
    (tmp_path / "example.txt").touch()

    result = service._find_docx_files()

    # Should return False because no files match _file_order
    assert result is False

    # _list_word_doc_files should be empty
    assert service._list_word_doc_files == []


def test_find_docx_files_no_files(service, tmp_path):
    # No files at all in folder
    result = service._find_docx_files()
    assert result is False
    assert service._list_word_doc_files == []
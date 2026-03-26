import pytest
from pathlib import Path
from fsniff.utils import load_config, find_files, process_file
from fsniff.factory import HandlerFactory
from fsniff.handlers.csv import CSVHandler

def test_handler_factory():
    csv_file = Path("test.csv")
    handler = HandlerFactory.get_handler(csv_file)
    assert isinstance(handler, CSVHandler)

def test_md5_calculation(tmp_path):
    d = tmp_path / "test.txt"
    content = "hello world"
    d.write_text(content)
    import hashlib
    expected = hashlib.md5(content.encode()).hexdigest()

    from fsniff.handlers.text import TextHandler
    handler = TextHandler(d, {})
    assert handler.calculate_md5() == expected

def test_empty_file_status(tmp_path):
    d = tmp_path / "empty.txt"
    d.touch()
    res = process_file(d, {})
    assert res['has_content'] is False
    assert res['size'] == 0

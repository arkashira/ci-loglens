import pytest
from ci_loglens import parse_log_file, ErrorSummary

def test_parse_log_file(tmp_path):
    log_file_path = tmp_path / "example.log"
    log_file_path.write_text("Error: something went wrong\nInfo: this is fine\nException: another error")
    error_summary = parse_log_file(log_file_path)
    assert error_summary.errors == ["Error: something went wrong", "Exception: another error"]

def test_parse_log_file_not_found():
    with pytest.raises(ValueError):
        parse_log_file("non_existent_log_file.log")

def test_parse_log_file_empty():
    log_file_path = "empty_log_file.log"
    with open(log_file_path, 'w') as file:
        file.write("")
    error_summary = parse_log_file(log_file_path)
    assert error_summary.errors == []

import pytest
from log_ingestion import LogIngestion, LogEntry

def test_upload_log():
    ingestion = LogIngestion()
    log_file = "This is a log message\nAnd another one"
    job_id = ingestion.upload_log(log_file)
    assert job_id == "0"

def test_upload_log_exceeds_limit():
    ingestion = LogIngestion()
    log_file = "a" * (200 * 1024 * 1024 + 1)
    with pytest.raises(ValueError):
        ingestion.upload_log(log_file)

def test_query_log():
    ingestion = LogIngestion()
    log_file = "This is a log message"
    job_id = ingestion.upload_log(log_file)
    result = ingestion.query_log(job_id)
    assert result["job_id"] == job_id

def test_search_logs():
    ingestion = LogIngestion()
    log_file = "This is a log message\nAnd another one with query"
    ingestion.upload_log(log_file)
    result = ingestion.search_logs("query")
    assert len(result["results"]) == 1

def test_search_logs_no_results():
    ingestion = LogIngestion()
    log_file = "This is a log message"
    ingestion.upload_log(log_file)
    result = ingestion.search_logs("nonexistent")
    assert len(result["results"]) == 0

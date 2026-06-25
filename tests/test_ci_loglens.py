import pytest
from ci_loglens import CiLoglens

def test_add_user():
    ci_loglens = CiLoglens()
    assert ci_loglens.add_user(1) == True
    assert ci_loglens.add_user(2) == True
    assert ci_loglens.free_tier_users == 2

def test_process_log_lines():
    ci_loglens = CiLoglens()
    ci_loglens.add_user(1)
    assert ci_loglens.process_log_lines(1, 5000) == True
    assert ci_loglens.process_log_lines(1, 0) == False

def test_get_usage_metrics():
    ci_loglens = CiLoglens()
    ci_loglens.add_user(1)
    ci_loglens.process_log_lines(1, 5000)
    metrics = ci_loglens.get_usage_metrics(1)
    assert metrics["log_lines_processed"] == 5000

def test_free_tier_limit():
    ci_loglens = CiLoglens()
    for i in range(100):
        ci_loglens.add_user(i)
    assert ci_loglens.add_user(100) == False

def test_log_lines_processed_limit():
    ci_loglens = CiLoglens()
    ci_loglens.add_user(1)
    assert ci_loglens.process_log_lines(1, 4000) == True
    assert ci_loglens.process_log_lines(1, 1000) == True

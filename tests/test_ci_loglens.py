import pytest
from ci_loglens import CiLoglens, ErrorCause
from datetime import datetime, timedelta

def test_get_top_error_causes():
    ci_loglens = CiLoglens()
    ci_loglens.add_error_cause("cause1", 0.9, datetime.now())
    ci_loglens.add_error_cause("cause2", 0.8, datetime.now())
    ci_loglens.add_error_cause("cause3", 0.7, datetime.now())
    top_causes = ci_loglens.get_top_error_causes()
    assert len(top_causes) == 3
    assert top_causes[0].confidence_score == 0.9

def test_filter_by_pipeline():
    ci_loglens = CiLoglens()
    ci_loglens.add_error_cause("pipeline1_cause1", 0.9, datetime.now())
    ci_loglens.add_error_cause("pipeline2_cause2", 0.8, datetime.now())
    ci_loglens.add_error_cause("pipeline1_cause3", 0.7, datetime.now())
    filtered_causes = ci_loglens.filter_by_pipeline("pipeline1")
    assert len(filtered_causes) == 2
    assert filtered_causes[0].cause == "pipeline1_cause1"

def test_filter_by_date_range():
    ci_loglens = CiLoglens()
    now = datetime.now()
    ci_loglens.add_error_cause("cause1", 0.9, now)
    ci_loglens.add_error_cause("cause2", 0.8, now - timedelta(days=1))
    ci_loglens.add_error_cause("cause3", 0.7, now + timedelta(days=1))
    filtered_causes = ci_loglens.filter_by_date_range(now - timedelta(days=1), now + timedelta(days=1))
    assert len(filtered_causes) == 2
    assert filtered_causes[0].cause == "cause1"

def test_filter_by_error_type():
    ci_loglens = CiLoglens()
    ci_loglens.add_error_cause("cause1_type1", 0.9, datetime.now())
    ci_loglens.add_error_cause("cause2_type2", 0.8, datetime.now())
    ci_loglens.add_error_cause("cause3_type1", 0.7, datetime.now())
    filtered_causes = ci_loglens.filter_by_error_type("type1")
    assert len(filtered_causes) == 2
    assert filtered_causes[0].cause == "cause1_type1"

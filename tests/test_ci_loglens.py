import pytest
from ci_loglens import CiLoglens, Error

def test_train_model():
    historical_failures = [
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 2', 'root_cause': 'Root Cause 2'}
    ]
    ci_loglens = CiLoglens(historical_failures)
    assert ci_loglens.classification_model['Error 1'] == ['Root Cause 1', 'Root Cause 1']

def test_suggest_root_cause():
    historical_failures = [
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 2', 'root_cause': 'Root Cause 2'}
    ]
    ci_loglens = CiLoglens(historical_failures)
    suggestion = ci_loglens.suggest_root_cause('Error 1')
    assert suggestion.root_cause == 'Root Cause 1'
    assert suggestion.confidence_score == 1.0

def test_suggest_root_cause_unknown_error():
    historical_failures = [
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 2', 'root_cause': 'Root Cause 2'}
    ]
    ci_loglens = CiLoglens(historical_failures)
    suggestion = ci_loglens.suggest_root_cause('Unknown Error')
    assert suggestion.root_cause is None
    assert suggestion.confidence_score == 0.0

def test_display_suggestions():
    historical_failures = [
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 1', 'root_cause': 'Root Cause 1'},
        {'error_message': 'Error 2', 'root_cause': 'Root Cause 2'}
    ]
    ci_loglens = CiLoglens(historical_failures)
    errors = ['Error 1', 'Error 2']
    ci_loglens.display_suggestions(errors)

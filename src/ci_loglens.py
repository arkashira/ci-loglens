import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Error:
    message: str
    root_cause: str = None
    confidence_score: float = 0.0
    documentation_link: str = None

class CiLoglens:
    def __init__(self, historical_failures: List[Dict]):
        self.historical_failures = historical_failures
        self.classification_model = self.train_model()

    def train_model(self):
        # Simple classification model based on historical failures
        model = {}
        for failure in self.historical_failures:
            error_message = failure['error_message']
            root_cause = failure['root_cause']
            if error_message not in model:
                model[error_message] = []
            model[error_message].append(root_cause)
        return model

    def suggest_root_cause(self, error_message: str) -> Error:
        if error_message in self.classification_model:
            root_causes = self.classification_model[error_message]
            most_common_root_cause = max(set(root_causes), key=root_causes.count)
            confidence_score = root_causes.count(most_common_root_cause) / len(root_causes)
            return Error(error_message, most_common_root_cause, confidence_score, 'https://example.com/docs')
        else:
            return Error(error_message)

    def display_suggestions(self, errors: List[str]):
        for error in errors:
            suggestion = self.suggest_root_cause(error)
            print(f'Error: {suggestion.message}')
            print(f'Suggested Root Cause: {suggestion.root_cause} (Confidence Score: {suggestion.confidence_score})')
            print(f'Documentation Link: {suggestion.documentation_link}')
            print('---')

import json 
from dataclasses import dataclass 
from datetime import datetime, timedelta
from typing import List

@dataclass
class ErrorCause:
    cause: str
    confidence_score: float
    timestamp: datetime

class CiLoglens:
    def __init__(self):
        self.error_causes = []

    def add_error_cause(self, cause: str, confidence_score: float, timestamp: datetime):
        self.error_causes.append(ErrorCause(cause, confidence_score, timestamp))

    def get_top_error_causes(self, num_causes: int = 5) -> List[ErrorCause]:
        return sorted(self.error_causes, key=lambda x: x.confidence_score, reverse=True)[:num_causes]

    def filter_by_pipeline(self, pipeline: str) -> List[ErrorCause]:
        return [cause for cause in self.error_causes if cause.cause.startswith(pipeline)]

    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> List[ErrorCause]:
        return [cause for cause in self.error_causes if start_date <= cause.timestamp < end_date]

    def filter_by_error_type(self, error_type: str) -> List[ErrorCause]:
        return [cause for cause in self.error_causes if cause.cause.endswith(error_type)]

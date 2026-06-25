import argparse
import json
import dataclasses
from datetime import datetime
from typing import Dict

@dataclasses.dataclass
class LogEntry:
    timestamp: str
    message: str

class LogIngestion:
    def __init__(self):
        self.logs = []
        self.job_id_counter = 0

    def upload_log(self, log_file: str) -> str:
        if len(log_file) > 200 * 1024 * 1024:
            raise ValueError("Log file exceeds 200 MB limit")

        log_entries = []
        for line in log_file.splitlines():
            log_entries.append(LogEntry(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message=line))

        job_id = str(self.job_id_counter)
        self.job_id_counter += 1
        self.logs.append({"job_id": job_id, "log_entries": log_entries})

        return job_id

    def query_log(self, job_id: str) -> Dict:
        for log in self.logs:
            if log["job_id"] == job_id:
                return log
        return {}

    def search_logs(self, query: str) -> Dict:
        results = []
        for log in self.logs:
            for entry in log["log_entries"]:
                if query in entry.message:
                    results.append({"job_id": log["job_id"], "log_entry": entry})
        return {"results": results}

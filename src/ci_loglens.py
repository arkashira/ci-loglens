import json
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class User:
    id: int
    log_lines_processed: int
    created_at: datetime

class CiLoglens:
    def __init__(self):
        self.users = {}
        self.free_tier_limit = 100
        self.free_tier_users = 0

    def add_user(self, user_id):
        if self.free_tier_users < self.free_tier_limit:
            self.users[user_id] = User(user_id, 0, datetime.now())
            self.free_tier_users += 1
            return True
        return False

    def process_log_lines(self, user_id, log_lines):
        if user_id in self.users:
            user = self.users[user_id]
            user.log_lines_processed += log_lines
            if log_lines == 0:
                return False
            return True
        return False

    def get_usage_metrics(self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            return {
                "log_lines_processed": user.log_lines_processed,
                "created_at": user.created_at.isoformat()
            }
        return None

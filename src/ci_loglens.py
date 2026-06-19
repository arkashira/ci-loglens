import argparse
import json
from dataclasses import dataclass
from typing import List

@dataclass
class ErrorSummary:
    errors: List[str]

def parse_log_file(log_file_path: str) -> ErrorSummary:
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()
            # Simple AI parser: extract lines containing "error" or "exception"
            error_lines = [line.strip() for line in log_content.splitlines() if "error" in line.lower() or "exception" in line.lower()]
            return ErrorSummary(errors=error_lines)
    except FileNotFoundError:
        raise ValueError(f"Log file not found: {log_file_path}")

def main():
    parser = argparse.ArgumentParser(description="CI Log Lens")
    parser.add_argument("--log", help="Path to log file", required=True)
    args = parser.parse_args()
    error_summary = parse_log_file(args.log)
    print(json.dumps({"errors": error_summary.errors}, indent=4))

if __name__ == "__main__":
    main()

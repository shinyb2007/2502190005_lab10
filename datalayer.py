"""
datalayer.py · Core data ingestion and validation module.
CS-1281 Python Programming Lab
"""

import os
import re

# Strict telemetry pattern
RECORD = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\|(?P<pump_id>PUMP-\d{2})\|(?P<voltage>\d+)\|(?P<current>\d+(?:\.\d+)?)\|(?P<status>[A-Z]+)$"
)


def parse_record(line: str) -> dict:
    cleaned = line.strip()
    if not cleaned:
        raise ValueError("Empty or blank line")

    match = RECORD.match(cleaned)
    if not match:
        raise ValueError(
            "Malformed syntax: Expected YYYY-MM-DD|PUMP-XX|VOLTAGE|CURRENT|STATUS"
        )

    data = match.groupdict()
    voltage = int(data["voltage"])
    current = float(data["current"])

    # Physical operating envelope checks
    if not (160 <= voltage <= 280):
        raise ValueError(
            f"Physical domain violation: Voltage {voltage}V outside safe limits (160-280V)"
        )
    if not (0.0 <= current <= 40.0):
        raise ValueError(
            f"Physical domain violation: Current {current}A outside safe limits (0-40A)"
        )

    return {
        "date": data["date"],
        "pump_id": data["pump_id"],
        "voltage": voltage,
        "current": current,
        "status": data["status"],
    }


def load(path: str) -> tuple[list[dict], list[tuple[int, str, str]]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input telemetry file not found: '{path}'")

    records = []
    problems = []

    with open(path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            raw_text = raw_line.rstrip("\r\n")
            try:
                record = parse_record(raw_text)
                records.append(record)
            except ValueError as err:
                problems.append((line_no, str(err), raw_text))

    return records, problems


def summarise(records: list[dict]) -> dict:
    total = len(records)
    if total == 0:
        return {
            "total": 0,
            "pumps": {},
            "statuses": {},
            "avg_v": 0.0,
            "avg_i": 0.0,
        }

    pumps = {}
    statuses = {}
    total_v = 0
    total_i = 0.0

    for r in records:
        pumps[r["pump_id"]] = pumps.get(r["pump_id"], 0) + 1
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
        total_v += r["voltage"]
        total_i += r["current"]

    return {
        "total": total,
        "pumps": pumps,
        "statuses": statuses,
        "avg_v": round(total_v / total, 1),
        "avg_i": round(total_i / total, 2),
    }
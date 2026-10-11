"""Read CommunityReach UTF-8 CSV files: name,cost,beneficiaries.
The beneficiaries field contains semicolon-separated anonymized identifiers.
"""
import csv
from pathlib import Path
from .core import Activity, validate


def read_activities(file_or_path):
    if isinstance(file_or_path, (str, bytes, Path)) or hasattr(file_or_path, "__fspath__"):
        with open(file_or_path, encoding="utf-8-sig", newline="") as stream:
            return _parse(stream)
    return _parse(file_or_path)


def _parse(stream):
    reader = csv.DictReader(stream)
    required = {"name", "cost", "beneficiaries"}
    if reader.fieldnames is None or not required.issubset(reader.fieldnames):
        raise ValueError("CSV must contain name,cost,beneficiaries columns")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError("Duplicate CSV column headers are not allowed")
    items = []
    for line, row in enumerate(reader, start=2):
        if None in row or any(row.get(col) is None for col in required):
            raise ValueError(f"Malformed CSV row at line {line}")
        name = row["name"].strip()
        if not name:
            raise ValueError(f"Missing activity name at line {line}")
        raw_cost = row["cost"].strip()
        try:
            cost = int(raw_cost)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid integer cost at line {line}") from None
        if cost <= 0:
            raise ValueError(f"Cost must be positive at line {line}")
        ids = frozenset(x.strip() for x in row["beneficiaries"].split(";") if x.strip())
        if not ids:
            raise ValueError(f"At least one beneficiary ID required at line {line}")
        items.append(Activity(name, cost, ids))
    if not items:
        raise ValueError("CSV has no activity rows")
    validate(items, 0)
    return items

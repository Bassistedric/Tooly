"""Prepare a reviewable, non-destructive Tooly equipment import from the Outillage extraction.

Usage:
 python -m scripts.prepare_equipment_import input.csv --output staged.csv --issues issues.csv
No database writes are performed.
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

def clean(value):
    return (value or "").strip()

def prepare(source: Path, output: Path, issues: Path):
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    numbers = Counter(clean(row.get("D")) for row in rows if clean(row.get("D")))
    staged, warnings = [], []
    for row in rows:
        origin = clean(row.get("source")).upper()
        source_row = clean(row.get("source_row"))
        key = f"{origin}:{source_row}"
        description = clean(row.get("A"))
        number = clean(row.get("D"))
        technique = clean(row.get("G")).upper()
        if origin == "ELEC":
            trade = "ELEC"
        elif "REF" in technique or "FROID" in technique:
            trade = "REF"
        elif "HVAC" in technique or "CHAUF" in technique or "VENT" in technique:
            trade = "HVAC"
        else:
            trade = "TO_REVIEW"
        status = clean(row.get("T")).upper()
        flags = []
        if not description: flags.append("MISSING_DESCRIPTION")
        if not number: flags.append("MISSING_NUMBER")
        elif numbers[number] > 1: flags.append("DUPLICATE_NUMBER")
        if trade == "TO_REVIEW": flags.append("TRADE_TO_REVIEW")
        if status not in ("OK", "NOK", "EN COURS", ""): flags.append("STATUS_TO_REVIEW")
        staged.append({
            "source_key": key,
            "source_file_group": origin,
            "source_row": source_row,
            "trade": trade,
            "original_number": number,
            "description": description,
            "model": clean(row.get("B")),
            "brand": clean(row.get("C")),
            "serial_number": clean(row.get("E")),
            "site": clean(row.get("F")),
            "technique_original": clean(row.get("G")),
            "holder_or_location": clean(row.get("H")),
            "user": clean(row.get("I")),
            "source_status": clean(row.get("T")),
            "source_notes": clean(row.get("V")),
            "review_flags": "|".join(flags),
        })
        if flags:
            warnings.append({"source_key": key, "flags": "|".join(flags), "number": number, "description": description})
    for path, data, fields in (
        (output, staged, list(staged[0]) if staged else ["source_key"]),
        (issues, warnings, ["source_key", "flags", "number", "description"]),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
    print(f"Prepared {len(staged)} source rows; {len(warnings)} rows require review. No database writes.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("staged_equipment.csv"))
    parser.add_argument("--issues", type=Path, default=Path("equipment_issues.csv"))
    args = parser.parse_args()
    prepare(args.input, args.output, args.issues)

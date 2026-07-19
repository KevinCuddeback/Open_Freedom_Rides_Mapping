#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "pilot"

REQUIRED_FIELDS = {
    "riders.json": {"id", "name", "birth_date", "tags"},
    "locations.json": {"id", "name", "latitude", "longitude", "precision"},
    "sources.json": {"id", "title", "type", "url_or_citation"},
    "events.json": {
        "id",
        "event_type",
        "date",
        "date_precision",
        "rider_ids",
        "location_id",
        "description",
        "source_refs",
    },
}


def load_table(name: str) -> list[dict]:
    with (RAW / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_required_fields(name: str, rows: list[dict], errors: list[str]) -> None:
    required = REQUIRED_FIELDS[name]
    for index, row in enumerate(rows, start=1):
        missing = sorted(required.difference(row.keys()))
        if missing:
            errors.append(f"{name}[{index}] missing required fields: {', '.join(missing)}")


def validate_unique_ids(name: str, rows: list[dict], errors: list[str]) -> None:
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        row_id = row.get("id")
        if row_id in seen:
            errors.append(f"{name}[{index}] duplicate id: {row_id}")
        seen.add(row_id)


def validate_dates(events: list[dict], riders: list[dict], errors: list[str]) -> None:
    for row in events:
        try:
            date.fromisoformat(row["date"])
        except Exception:
            errors.append(f"events invalid ISO date: {row.get('id')} => {row.get('date')}")

    for row in riders:
        try:
            date.fromisoformat(row["birth_date"])
        except Exception:
            errors.append(f"riders invalid birth_date: {row.get('id')} => {row.get('birth_date')}")


def validate_coordinates(locations: list[dict], errors: list[str]) -> None:
    for row in locations:
        lat = row.get("latitude")
        lon = row.get("longitude")
        if not isinstance(lat, (int, float)) or not -90 <= lat <= 90:
            errors.append(f"locations invalid latitude: {row.get('id')} => {lat}")
        if not isinstance(lon, (int, float)) or not -180 <= lon <= 180:
            errors.append(f"locations invalid longitude: {row.get('id')} => {lon}")


def validate_references(
    events: list[dict],
    riders: list[dict],
    locations: list[dict],
    sources: list[dict],
    errors: list[str],
) -> None:
    rider_ids = {row["id"] for row in riders}
    location_ids = {row["id"] for row in locations}
    source_ids = {row["id"] for row in sources}

    for row in events:
        if row.get("location_id") not in location_ids:
            errors.append(f"event {row.get('id')} references unknown location_id {row.get('location_id')}")

        for rider_id in row.get("rider_ids", []):
            if rider_id not in rider_ids:
                errors.append(f"event {row.get('id')} references unknown rider_id {rider_id}")

        for source_ref in row.get("source_refs", []):
            if source_ref.get("source_id") not in source_ids:
                errors.append(
                    f"event {row.get('id')} references unknown source_id {source_ref.get('source_id')}"
                )


def main() -> int:
    errors: list[str] = []

    riders = load_table("riders.json")
    locations = load_table("locations.json")
    sources = load_table("sources.json")
    events = load_table("events.json")

    tables = {
        "riders.json": riders,
        "locations.json": locations,
        "sources.json": sources,
        "events.json": events,
    }

    for name, rows in tables.items():
        validate_required_fields(name, rows, errors)
        validate_unique_ids(name, rows, errors)

    validate_dates(events, riders, errors)
    validate_coordinates(locations, errors)
    validate_references(events, riders, locations, sources, errors)

    if errors:
        print("Validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

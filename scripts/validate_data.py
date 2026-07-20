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

ALLOWED_DATE_PRECISIONS = {"day", "month", "year", "unknown"}
ALLOWED_LOCATION_PRECISIONS = {"facility", "city", "region", "approximate"}
ALLOWED_EVENT_TYPES = {"departure", "arrival", "stop", "incident", "arrest", "detention", "meeting"}
ALLOWED_GEOMETRY_CONFIDENCE = {"high", "medium", "low", "unknown"}


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


def validate_enums_and_completeness(events: list[dict], locations: list[dict], errors: list[str]) -> None:
    for row in locations:
        precision = row.get("precision")
        if precision not in ALLOWED_LOCATION_PRECISIONS:
            errors.append(
                f"location {row.get('id')} has invalid precision {precision}; "
                f"allowed: {', '.join(sorted(ALLOWED_LOCATION_PRECISIONS))}"
            )

    for row in events:
        date_precision = row.get("date_precision")
        if date_precision not in ALLOWED_DATE_PRECISIONS:
            errors.append(
                f"event {row.get('id')} has invalid date_precision {date_precision}; "
                f"allowed: {', '.join(sorted(ALLOWED_DATE_PRECISIONS))}"
            )

        event_type = row.get("event_type")
        if event_type not in ALLOWED_EVENT_TYPES:
            errors.append(
                f"event {row.get('id')} has invalid event_type {event_type}; "
                f"allowed: {', '.join(sorted(ALLOWED_EVENT_TYPES))}"
            )

        geometry_confidence = row.get("geometry_confidence", "unknown")
        if geometry_confidence not in ALLOWED_GEOMETRY_CONFIDENCE:
            errors.append(
                f"event {row.get('id')} has invalid geometry_confidence {geometry_confidence}; "
                f"allowed: {', '.join(sorted(ALLOWED_GEOMETRY_CONFIDENCE))}"
            )

        rider_ids = row.get("rider_ids")
        if not isinstance(rider_ids, list) or len(rider_ids) == 0:
            errors.append(f"event {row.get('id')} must include at least one rider_id")

        source_refs = row.get("source_refs")
        if not isinstance(source_refs, list) or len(source_refs) == 0:
            errors.append(f"event {row.get('id')} must include at least one source_ref")
        else:
            for index, source_ref in enumerate(source_refs, start=1):
                source_id = source_ref.get("source_id")
                note = source_ref.get("note")
                if not isinstance(source_id, str) or not source_id.strip():
                    errors.append(f"event {row.get('id')} source_refs[{index}] has empty source_id")
                if not isinstance(note, str) or not note.strip():
                    errors.append(f"event {row.get('id')} source_refs[{index}] has empty note")

        inference = row.get("inference", {})
        is_inferred = inference.get("is_inferred")
        reason = inference.get("reason")
        if is_inferred is True and not isinstance(reason, str):
            errors.append(f"event {row.get('id')} inferred event must provide a reason")
        if is_inferred is False and reason not in (None, ""):
            errors.append(
                f"event {row.get('id')} non-inferred event should set inference.reason to null or empty"
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
    validate_enums_and_completeness(events, locations, errors)

    if errors:
        print(f"Validation FAILED ({len(errors)} issue(s) detected)")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

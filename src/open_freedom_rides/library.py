from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Dataset:
    riders: list[dict[str, Any]]
    locations: list[dict[str, Any]]
    sources: list[dict[str, Any]]
    events: list[dict[str, Any]]


def _load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_dataset(base_path: Path) -> Dataset:
    """Load pilot raw dataset tables from a directory."""
    return Dataset(
        riders=_load_json(base_path / "riders.json"),
        locations=_load_json(base_path / "locations.json"),
        sources=_load_json(base_path / "sources.json"),
        events=sorted(_load_json(base_path / "events.json"), key=lambda e: (e["date"], e["id"])),
    )


def events_for_rider(dataset: Dataset, rider_id: str) -> list[dict[str, Any]]:
    return [e for e in dataset.events if rider_id in e.get("rider_ids", [])]


def riders_at_location(dataset: Dataset, location_id: str) -> list[dict[str, Any]]:
    rider_ids: set[str] = {
        rider_id
        for event in dataset.events
        if event.get("location_id") == location_id
        for rider_id in event.get("rider_ids", [])
    }
    return [r for r in dataset.riders if r["id"] in rider_ids]


def events_in_date_range(dataset: Dataset, start_date: str, end_date: str) -> list[dict[str, Any]]:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    return [
        e
        for e in dataset.events
        if start <= date.fromisoformat(e["date"]) <= end
    ]


def journey_segments_for_rider(dataset: Dataset, rider_id: str) -> list[dict[str, Any]]:
    rider_events = events_for_rider(dataset, rider_id)
    locations_by_id = {l["id"]: l for l in dataset.locations}

    segments: list[dict[str, Any]] = []
    for index in range(len(rider_events) - 1):
        current_event = rider_events[index]
        next_event = rider_events[index + 1]
        current_location = locations_by_id.get(current_event["location_id"])
        next_location = locations_by_id.get(next_event["location_id"])
        if not current_location or not next_location:
            continue

        segments.append(
            {
                "segment_id": f"seg-{rider_id}-{index + 1:03d}",
                "rider_id": rider_id,
                "from_event_id": current_event["id"],
                "to_event_id": next_event["id"],
                "from_location_id": current_event["location_id"],
                "to_location_id": next_event["location_id"],
                "from": [current_location["longitude"], current_location["latitude"]],
                "to": [next_location["longitude"], next_location["latitude"]],
                "date_start": current_event["date"],
                "date_end": next_event["date"],
                "derived_from_events": [current_event["id"], next_event["id"]],
            }
        )
    return segments

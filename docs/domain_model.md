# Domain Model

## Core entities

- **Rider**: Person participating in one or more Freedom Ride segments.
- **Location**: Geospatial place tied to events (city/facility/approximate area).
- **Source**: Archival or published evidence supporting historical claims.
- **Event**: Time-bound historical fact connecting riders, locations, and sources.

## Relationship model

- A rider participates in many events (`events.rider_ids`).
- An event happens at one location (`events.location_id`).
- An event cites one or more sources (`events.source_refs[].source_id`).
- Rider journey segments are **derived** from ordered event sequences.

## Temporal rules

- `date` is ISO-8601 (`YYYY-MM-DD`) in the pilot.
- `date_precision` indicates confidence granularity (day/month/year/unknown).
- Inferred timing is represented via `inference` metadata.

## Spatial rules

- Coordinates are WGS84 decimal degrees.
- `precision` captures location granularity (facility/city/region/approximate).
- `geometry_confidence` on events documents certainty of mapped placement.

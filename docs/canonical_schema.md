# Canonical Schema

The canonical schema separates hand-authored historical facts from generated geospatial artifacts.

## Raw tables (authoritative)

- `riders.json`
- `locations.json`
- `sources.json`
- `events.json`

All records must use stable IDs and source-backed provenance.

## Derived outputs (generated)

- `rider_journeys.geojson`
- Map SVG files and Commons sidecar metadata

Derived outputs must never be manually edited.

## Provenance requirements

Every event includes:
- `source_refs[]` entries
- Citation note per source reference
- Inference metadata for interpretation boundaries

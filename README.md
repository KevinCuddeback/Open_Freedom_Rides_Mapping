# Open Freedom Rides Mapping

Open Freedom Rides Mapping is a structured data-and-tooling library for documenting Freedom Rides history as source-cited, geospatially usable records.

## Project Boundary (v0 Pilot)

This repository is a **monorepo focused on a reusable data library + map-generation pipeline**.

Current pilot outputs:
- Wikimedia Commons-ready SVG map artifacts
- GeoJSON exports for academic/civic GIS workflows
- Rider-specific journey reconstructions from shared historical event data

Initial pilot scope:
- Time period: May 1961 pilot window
- Riders: a small starter set for schema and pipeline validation
- Geography: core route nodes in Washington, D.C., Richmond, and Charlotte
- Facilities/incidents: represented through event typing and source-backed provenance

## Repository Layout

- `src/open_freedom_rides/` — reusable Python library and query API
- `scripts/` — ingestion validation and output generation workflows
- `data/raw/pilot/` — hand-authored, source-cited pilot records
- `data/derived/pilot/` — generated geospatial outputs (GeoJSON)
- `assets/generated/pilot/` — generated visual outputs (SVG + Commons sidecar metadata)
- `assets/templates/` — Wikimedia metadata templates
- `docs/` — domain model, contributor workflow, milestones

## Data Model Highlights

Core entities in the pilot:
- riders
- locations
- sources
- events

Derived entities in pipeline output:
- rider route segments
- rider journey tracks

Model principles:
- Stable IDs (`rider-*`, `loc-*`, `evt-*`, `src-*`)
- Provenance on historical claims via `source_refs`
- Explicit uncertainty fields for date/location confidence
- Separation between source-backed facts and derived geospatial artifacts

## Workflows

### 1) Validate raw data

```bash
python scripts/validate_data.py
```

Runs required-field checks, referential integrity checks, duplicate ID checks, date format checks, and coordinate range checks.

### 2) Build derived outputs

```bash
python scripts/build_outputs.py
```

Generates:
- `data/derived/pilot/rider_journeys.geojson`
- `assets/generated/pilot/freedom_rides_pilot.svg`
- `assets/generated/pilot/freedom_rides_pilot.commons.wikitext`

### 3) Query via library API

```python
from pathlib import Path
from open_freedom_rides import load_dataset, events_for_rider

dataset = load_dataset(Path("data/raw/pilot"))
rider_events = events_for_rider(dataset, "rider-john-lewis")
```

## Licensing

This project is dual-licensed to support both open-source software development and free cultural reuse on Wikimedia platforms:

- **Source Code:** All automation scripts, library source files, and configuration files are licensed under the [MIT License](LICENSE-CODE).
- **Data and Visual Assets:** All dataset tables (JSON/CSV/GeoJSON) and generated map graphics (SVG/PNG), plus Wikimedia upload sidecars, are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License](LICENSE-DATA).

When publishing to Wikimedia Commons, generated metadata should include `{{CC-BY-SA-4.0}}`.

## Milestones

See `docs/milestones.md` for phased delivery from pilot bootstrap through expanded API/data coverage.

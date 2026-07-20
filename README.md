# Open Freedom Rides Mapping Project (OFRMP)

An open-source, relational, spatiotemporal data ecosystem that documents the 1961 Freedom Rides movement — transforming historical narratives into precise geospatial nodes and edges to power Wikimedia Commons SVG maps, interactive academic maps, and deeply personalized journey tracks for individual riders.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Repository Structure](#repository-structure)
- [Data Model](#data-model)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Roadmap](#roadmap)
- [Licenses](#licenses)
- [Contributing](#contributing)

---

## About the Project

The Open Freedom Rides Mapping Project (OFRMP) builds a rigorous, machine-readable record of every rider, transit segment, carrier, incident, and facility that made up the Freedom Rides campaign of 1961. The foundational source of truth is Raymond Arsenault's *Freedom Riders: 1961 and the Struggle for Racial Justice*.

**Core objectives:**

- Parse narrative history into four flat relational tables: **Riders**, **Transit Links**, **Carriers**, and **Incidents**.
- Cross-link every rider and location to external open archives: MSSC surveillance files, MDAH arrest records, CRMvet.org veteran rosters, AAPB oral-history audio/video, and CRDL media records.
- Align activist routes with the real 1961 transportation network using historic Greyhound, National Trailways, Illinois Central Railroad, and Louisville & Nashville Railroad timetables.
- Produce clean, un-pixelated W3C SVG maps scalable for both Wikipedia infoboxes and high-resolution print publications.
- Power a client-side interactive map (OpenLayers or MapLibre GL JS) with biographical filtering, transport-system toggles, and a trauma/sensitivity control.

---

## Repository Structure

```
.
├── data/
│   ├── raw/pilot/          # Hand-authored source JSON (riders, locations, events, sources)
│   └── derived/            # Generated outputs — do NOT edit manually
├── docs/
│   ├── canonical_schema.md # Authoritative field-level schema documentation
│   ├── contributing.md     # Contributor workflow guide
│   ├── domain_model.md     # Entity and relationship model
│   └── milestones.md       # Project milestone tracker
├── schemas/
│   └── ofrmp.schema.json   # Unified JSON schema / data dictionary
├── scripts/
│   ├── validate_data.py    # Validates raw data against the JSON schema
│   └── build_outputs.py    # Generates derived GeoJSON, CSV, and SVG assets
├── src/
│   └── open_freedom_rides/ # Python library (validation helpers, pipeline utilities)
├── assets/
│   └── generated/          # Generated SVG maps and export packages
├── tests/                  # Unit tests for the Python library
├── PROJECT_INITIATION_AND_SPECIFICATION_SYSTEM.txt  # Full project specification
├── Makefile
└── pyproject.toml
```

---

## Data Model

Four core entities underpin the dataset:

| Entity | Description |
|---|---|
| **Rider** | Every participant — name, affiliation (CORE, SNCC, SCLC, NAACP), gender, home city, birth/death years |
| **Location** | Geospatial place (bus depot, train station, airfield, ambush site) with WGS84 coordinates and 1961-era precision |
| **Event** | Time-bound historical fact linking one or more riders to a location with full source provenance |
| **Source** | Archival or published citation supporting each event claim |

Rider journey segments are **derived** from ordered event sequences — they are never hand-authored. See [`docs/domain_model.md`](docs/domain_model.md) for full relationship rules and temporal/spatial confidence conventions.

---

## Getting Started

**Requirements:** Python 3.10+

```bash
# Install the library and dependencies
pip install -e .

# Validate all raw data against the schema
make validate

# Generate derived outputs (GeoJSON, CSV, SVG)
make build

# Run the test suite
make test
```

---

## Development Workflow

1. Edit raw data files in `data/raw/pilot/` (riders, locations, events, sources).
2. Run `make validate` to confirm schema compliance.
3. Run `make build` to regenerate derived outputs in `data/derived/` and `assets/generated/`.
4. Commit both the raw edits **and** the regenerated outputs together.

> **Never manually edit files under `data/derived/` or `assets/generated/`.** These are always regenerated from the raw sources.

Full contributor instructions: [`docs/contributing.md`](docs/contributing.md)

---

## Roadmap

### ✅ Milestone 1 — Scaffold (complete)
- Repository structure and dual-license setup
- Domain model, JSON schema, and documentation
- Contributor workflow guide

### 🔄 Milestone 2 — Pilot Dataset (in progress)
- Expand rider, location, event, and source records for the pilot dataset
- Harden schema validation checks and improve data completeness
- Establish ingestion foundations for rider, station/facility, carrier, and segment records (spidering, downloading, normalization contracts)

### 🔜 Milestone 3 — Geospatial Enrichment
- Improve route-building semantics for journey interruptions and overlaps
- Add richer derived GeoJSON exports with confidence metadata

### 🔜 Milestone 4 — Wikimedia SVG Pipeline
- Improve SVG styling, labeling, and scale fidelity for Wikimedia Commons
- Add reusable map templates for additional route sets
- Automate Wikipedia information-template sidecars for bulk upload

### 🔜 Milestone 5 — Public Distribution
- Expand public query API and dataset coverage
- Add bulk filtering and compressed packaging for educators, archivists, and GIS users

---

## Licenses

| Asset type | License |
|---|---|
| Source code | [MIT License](LICENSE-CODE) |
| Data (JSON, CSV, GeoJSON, SVG) | [Creative Commons CC0 1.0 Public Domain](LICENSE-DATA) |

The CC0 dedication removes all intellectual-property barriers so historians, educators, and researchers worldwide can reuse the dataset without restriction.

---

## Contributing

Contributions of all kinds are welcome — historical data, source citations, code improvements, and documentation fixes. Please read [`docs/contributing.md`](docs/contributing.md) before submitting a pull request.

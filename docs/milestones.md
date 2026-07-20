# Milestones

## Milestone 1 (implemented scaffold)
- Repository structure and dual-license setup
- Domain model and schema documentation
- Contributor workflow guide

## Milestone 2 (current focus: ingestion foundation)
- Expand rider/location/event/source pilot dataset
- Harden validation checks and schema completeness
- Stand up a reproducible ingestion path for rider, station/facility, carrier, and segment facts

### Milestone 2A — Spidering and source inventory
- Define the priority source list (books, archival collections, timetable scans, carrier maps, arrest logs).
- Build a source registry that records where each source was found, access constraints, and refresh cadence.
- Capture extraction boundaries up front (what is transcribed verbatim vs inferred).

### Milestone 2B — Downloading and provenance capture
- Create a deterministic download manifest (source URL/location, retrieval date, checksum, license/rights note).
- Store immutable raw snapshots before any cleanup so normalization can be re-run.
- Track source-level quality flags (scan legibility, OCR confidence, missing pages/editions).

### Milestone 2C — Normalization contract
- Define stable ID rules for riders, facilities/stations, carriers, and segments.
- Define crosswalks from current `events` records to future segment-centric records.
- Define normalization rules for names, aliases, dates, and route references.
- Add required uncertainty fields for inferred timing, inferred geometry, and disputed claims.

### What we need to learn now to unlock later milestones
- **Entity resolution risk:** how often rider names, station names, and carrier names collide across sources.
- **Temporal granularity limits:** where only month/year or sequence order is known and how that affects segment chaining.
- **Spatial precision limits:** which facilities can be geocoded to exact historical addresses vs city-level approximations.
- **Carrier hierarchy reality:** how often a route references parent networks vs regional operators in primary evidence.
- **Segment boundary rules:** when to split or merge segments around transfers, arrests, and interruptions.

### Milestone 2 exit criteria
- Source registry and download manifest are in place and documented.
- Normalization rules are explicit enough for repeatable ingest runs.
- Pilot records demonstrate rider + facility + carrier + segment linkage with provenance.
- Open questions are tracked as explicit schema/doc TODOs (not implicit assumptions).

## Milestone 3
- Improve route-building semantics for interruptions/overlaps
- Add richer derived geospatial exports

## Milestone 4
- Improve Wikimedia SVG styling and labeling quality
- Add reusable map templates for additional route sets

## Milestone 5
- Expand public query API and dataset coverage
- Add bulk filtering and packaging for downstream consumers

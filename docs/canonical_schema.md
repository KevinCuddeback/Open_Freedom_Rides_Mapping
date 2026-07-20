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

## Ingestion staging: current pilot -> target transit entities

The current pilot ingestion is event-centric (`riders`, `locations`, `sources`, `events`), while the target historical transit model is segment-centric (`riders`, `carriers`, `facilities`, `segments`).

To keep future migration low-risk, ingestion work should explicitly produce and preserve:

- **Stable identity crosswalks**  
  Rider aliases -> canonical rider IDs, historic station names -> canonical facility IDs, carrier brand names -> canonical carrier IDs.
- **Temporal normalization rules**  
  Exact timestamps when present, plus explicit handling for day/month/year/sequence-only evidence.
- **Spatial normalization rules**  
  Facility-level coordinates when provable, and explicit lower-precision geometry tags when only city/region evidence exists.
- **Segment derivation rules**  
  Clear logic for when events form one segment vs multiple segments (especially transfers, interruptions, arrests, and detentions).
- **Provenance retention at every transformation step**  
  Every normalized field should remain traceable to one or more source references and notes.

### Learning goals for this stage

Before scaling ingest volume, document what the pilot reveals about:

1. Alias frequency and ambiguity across riders, facilities, and carriers.
2. Typical OCR/transcription failure modes and cleanup requirements.
3. Coverage gaps in timetable/network sources that force inferred segment geometry.
4. The minimum metadata needed to regenerate normalized outputs deterministically.

## Provenance requirements

Every event includes:
- `source_refs[]` entries
- Citation note per source reference
- Inference metadata for interpretation boundaries

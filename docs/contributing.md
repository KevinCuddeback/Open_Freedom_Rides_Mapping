# Contributing Workflow

## Add or update source material

1. Add or update entries in `data/raw/pilot/sources.json`.
2. Use clear citation text in `url_or_citation`.

## Add or update riders, locations, or events

1. Update the corresponding raw JSON file.
2. Use stable IDs and preserve existing IDs.
3. Include provenance in `source_refs` for every event.
4. Mark uncertain claims in `inference` and confidence fields.

## Validate and regenerate outputs

1. Run `python scripts/validate_data.py`.
2. Run `python scripts/build_outputs.py`.
3. Commit both raw changes and regenerated derived outputs.

## Hand-authored vs generated files

- Hand-authored: `data/raw/**`, docs, templates, source code.
- Generated: `data/derived/**`, `assets/generated/**`.

Never manually edit generated outputs.


# Data acquisition and provenance

## Google Earth Engine
1. Create/select a Google Cloud project eligible for noncommercial Earth Engine use.
2. Register/verify it for Earth Engine.
3. Install requirements.
4. Run `earthengine authenticate`.
5. Set `GEE_PROJECT_ID=<project-id>` and `GEE_ENABLED=true` in `.env`.
6. Run `python scripts/check_gee_access.py`.

## UNOSAT reference
Use `python scripts/acquire_reference_data.py`, open each product page, and download the offered SHP/vector package when permitted. Preserve licences/metadata. Do **not** compare a cumulative multi-day footprint directly with a single Sentinel acquisition unless the methodology explicitly accounts for that temporal mismatch.

## Open-Meteo
No API key is required for the noncommercial free API, but rate limits and attribution apply. The flood API provides GloFAS discharge at about 5-km resolution and cautions that the nearest river might not be selected correctly.

## Reproducibility
Record every scene date, orbit pass, polarization, cloud threshold, dataset version, threshold and code commit. Export the final prediction/reference masks to the same grid before computing IoU/F1.

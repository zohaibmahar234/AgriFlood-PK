# Research Evaluation Report

## Status
**Blocked / not yet scientifically executed in this environment.**

### What is ready
- Time/location-specific 2022 Khairpur case-study design.
- Sentinel-1 baseline implementation.
- Cropland exposure implementation.
- Sentinel-2 NDVI recovery implementation.
- Metric plan: precision, recall, F1, IoU with common-grid/no-data handling.

### Why no accuracy numbers are reported
Authenticated Google Earth Engine access for the user's project was not available, and a suitable time-matched UNOSAT vector/raster was not downloaded into this environment. Reporting fabricated values would violate the research design.

### Required next scientific execution
1. Authenticate/verify GEE with `scripts/check_gee_access.py`.
2. Run `scripts/gee_flood_map.js` and record exact scene IDs/dates.
3. Download a temporally overlapping UNOSAT SHP/vector product (e.g., product 3349 or 3348 where appropriate).
4. Harmonize grids and compute TP/FP/FN metrics.
5. Document temporal mismatch and excluded areas.
6. Repeat with at least one held-out date/area if data permits.

### Forecast advisory
No forecasting accuracy is claimed. The rule is explicitly experimental and uncalibrated.

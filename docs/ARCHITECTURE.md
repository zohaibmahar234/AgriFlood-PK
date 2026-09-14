# Architecture and data flow

Browser (Leaflet UI) → FastAPI → three deliberately separate paths:
1. **Forecast advisory:** Open-Meteo rainfall + GloFAS discharge → interpretable experimental baseline → dashboard state.
2. **Observed flood:** Earth Engine Sentinel-1 → before/after change → permanent-water + terrain masks → flood candidate.
3. **Agricultural exposure:** observed flood candidate ∩ WorldCover cropland → area estimate labelled “potentially affected cropland”.
4. **Recovery:** Sentinel-2 SR + cloud probability → NDVI seasonal-baseline comparison on cropland.

SQLite stores alert state and prevents duplicate keys. Scientific rasters are processed remotely in Earth Engine; the dashboard should cache summaries/exports rather than reprocessing every page load.

Security: `.env` is excluded; no Earth Engine tokens are placed in frontend code. Exact farm geometry is outside the core scope and should be treated as sensitive if added later.

# AgriFlood-PK

Academic FYP prototype for **flood-risk advisory, satellite-observed flood mapping, potentially affected cropland, and crop-recovery monitoring** in Sindh, Pakistan. The initial study district is **Khairpur District** (city reference: **Khairpur Mir's**) because credible 2022 UNOSAT assessments include district-level flood evidence and imagery showing inundated agricultural areas around Khairpur city.

> **Safety / scope:** This software is an academic prototype. It is **not an official flood-warning service**. Forecast advisory, satellite-observed water, agricultural exposure, and vegetation recovery are deliberately reported as separate outputs.

## What runs without paid services
- FastAPI backend + SQLite cache / alerts.
- Lightweight Leaflet frontend (no Node build required; selected to keep RAM and setup low for an FYP laptop).
- Live Open-Meteo forecast and GloFAS river-discharge calls when internet is available.
- Offline historical replay using verified source metadata/statistics, clearly separated from scientific raster validation.
- Software tests using labelled synthetic fixtures.

## What requires your Google Earth Engine access
- Real Sentinel-1 before/after flood mapping.
- WorldCover cropland overlay and area computation.
- Sentinel-2 NDVI recovery processing.
- Export of scientific validation layers for comparison with UNOSAT reference data.

Google Earth Engine requires a registered/verified noncommercial Cloud project. Put the project id in `.env`; never commit credentials.

## Windows quick start
1. Install Python 3.11 or 3.12 (recommended) and Git. Python 3.13 may work but is not the documented target.
2. Open PowerShell in this folder.
3. `py -3.12 -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `pip install -r backend\requirements.txt`
6. `copy .env.example .env`
7. `python -m uvicorn backend.app.main:app --reload --port 8000`
8. Open `http://127.0.0.1:8000/` in your browser.

For Earth Engine setup, see `docs/WINDOWS_SETUP.md` and `docs/DATA_ACQUISITION.md`.

## Test
```powershell
pytest backend\tests -q
```

See `reports/SOFTWARE_TEST_REPORT.md` and `reports/RESEARCH_EVALUATION_REPORT.md` for what was actually verified in this delivery.

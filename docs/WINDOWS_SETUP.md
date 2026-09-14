# Windows installation and startup

## Recommended laptop target
- Windows 10/11 64-bit.
- Python 3.11–3.12.
- RAM: **8 GB minimum estimated**, **16 GB recommended estimated** for comfortable browser + IDE use.
- Free storage: **5 GB minimum** for code/caches; 15+ GB recommended if exporting several local GeoTIFFs.
- GPU: not required for the implemented baseline.

These are engineering estimates, not measured benchmarks from the user's laptop.

## Setup
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
copy .env.example .env
python -m uvicorn backend.app.main:app --reload --port 8000
```
Open `http://127.0.0.1:8000`.

## Earth Engine
```powershell
earthengine authenticate
$env:GEE_PROJECT_ID="your-project-id"
python scripts\check_gee_access.py
```
Then set the same project id and `GEE_ENABLED=true` in `.env`.

## Scheduling caveat
Any local scheduler/background worker runs only while the laptop is on and connected. This prototype therefore uses on-demand jobs + caching rather than pretending to provide always-on operational monitoring.

## Windows verification status
The code was built/tested in a Linux execution environment, **not on an actual Windows host**. Windows commands are documented but Windows execution remains unverified.

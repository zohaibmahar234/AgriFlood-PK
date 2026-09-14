# Software Test Report

## Environment
- Build/test OS: Linux container (Windows execution not available).
- Python runtime used for verification: 3.13.5.
- Node used only for JavaScript syntax check: 22.16.0.
- Documented deployment target: Python 3.11/3.12 on Windows 10/11.

## Executed checks
| Check | Result |
|---|---|
| Python compile (`python -m compileall -q backend scripts`) | PASS |
| Frontend JavaScript syntax (`node --check frontend/app.js`) | PASS |
| Pytest backend/data logic suite | PASS — 12 tests |
| FastAPI health endpoint | PASS — HTTP 200 |
| Frontend root served by FastAPI | PASS — HTTP 200 |
| Input validation | PASS |
| Experimental advisory high/low/unknown behavior | PASS |
| Missing data → Unknown/Insufficient Data | PASS |
| Duplicate alert key is updated, not duplicated | PASS |
| Expired alert becomes inactive | PASS |
| Provider failure is converted to useful HTTP 502 | PASS |
| Historical replay identifies itself as reference metadata, not synthetic scientific raster | PASS |
| GEE unavailable/configuration blocker produces explicit HTTP 503 | PASS |
| Precision/recall/F1/IoU helper math | PASS using clearly synthetic unit-test fixture only |

## Not executed / blockers
- Live Open-Meteo calls: not used as a deterministic test oracle because this execution environment does not provide general runtime network access.
- Google Earth Engine Sentinel jobs: not executed because the user's authenticated Earth Engine project was not available.
- Quantitative UNOSAT raster/vector comparison: not executed because a time-matched downloadable reference layer was not supplied/acquired in this runtime.
- Actual Windows installation/startup: not executed; instructions only.
- Browser interaction automation: not available; HTML/JS serving and JS syntax were verified, and API integration paths are covered by backend tests.

## Conclusion
The local software paths that do not require external authenticated/scientific services passed the executed checks. This report does not imply scientific validity of the flood-detection thresholds or forecast advisory.

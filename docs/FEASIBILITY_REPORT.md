# Feasibility Report — AgriFlood-PK

## Decision
**Initial study district: Khairpur District, Sindh (city reference: Khairpur Mir's).** Rationale: UNOSAT's 15-Aug-2022 Sindh assessment includes Khairpur District in its district table, and its 9-Sep-2022 flood-evolution assessment shows inundated agricultural areas around Khairpur city using 3-Sep imagery. These sources provide district-specific historical evidence suitable for a reproducible case study, while time-matched validation layers still need to be acquired and checked before quantitative accuracy claims.

## Earth Engine access
Current noncommercial Earth Engine use requires a registered/verified Cloud project. The Community tier is aimed at undergraduate students and provides a monthly noncommercial compute quota. This delivery cannot verify the user's own account/project because no authorization was provided. `scripts/check_gee_access.py` performs the verification locally after authentication.

## Candidate datasets
| Purpose | Dataset | Resolution / role | Notes |
|---|---|---|---|
| Flood observation | Sentinel-1 GRD `COPERNICUS/S1_GRD` | ~10 m selected products | SAR works through cloud; use consistent mode/polarization/orbit where practical. |
| Vegetation recovery | Sentinel-2 SR Harmonized | 10–20 m | Pair with cloud probability; seasonal baseline required. |
| Cropland mask | ESA WorldCover 2021 v200 | 10 m | Class 40 cropland; CC BY 4.0. |
| Permanent water | JRC Global Surface Water v1.4 | 30 m | Mask persistent water; attribution required. |
| Terrain | SRTM 30 m | 30 m | Used only as a false-positive reduction aid. |
| Boundary | FAO GAUL level 2 | district | Noncommercial licence; review redistribution conditions. |
| Reference | UNOSAT 3349 / 3348 / 3352 | mixed | Preliminary satellite reference; not perfect ground truth. |
| Weather | Open-Meteo | model-dependent | Noncommercial free API limits apply; attribution required. |
| River discharge | Open-Meteo GloFAS | ~5 km | API warns nearest river may not be selected correctly. |

## Basic flood-map milestone
A reproducible Earth Engine baseline is implemented in `scripts/gee_flood_map.js` and backend `backend/app/gee.py` using Sentinel-1 before/after change, permanent-water masking, a low-slope filter, and cropland overlay. **It was not executed here because user Earth Engine authentication/project access is unavailable.** Therefore no raster area result, precision/recall/F1/IoU, or validation success is claimed.

## Reference suitability warning
UNOSAT products may be cumulative, multi-day, different-sensor, or preliminary. A single-day Sentinel-1 product must be compared only to a spatial/temporal reference that sufficiently overlaps that observation. Cumulative national extent is context, not direct pixel-level truth for one scene.

## Feasibility conclusion
The project is technically feasible as an academic prototype. The only current core scientific blocker is authenticated Earth Engine execution plus acquisition of a time-matched reference vector/raster for quantitative validation. Software, historical-source replay, weather/discharge integration, alerts, and test infrastructure can proceed independently.

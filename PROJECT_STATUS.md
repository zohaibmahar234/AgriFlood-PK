# AgriFlood-PK — Project Status

**Project:** AgriFlood-PK: Flood Detection and Crop Recovery Monitoring in Sindh  
**Study Area:** Khairpur District, Sindh, Pakistan  
**Project Type:** Final Year Project (FYP)  
**Status:** Active Development

---

## Current Objective

AgriFlood-PK aims to develop a satellite-based framework for:

- Flood extent detection
- Agricultural exposure assessment
- Post-flood crop recovery monitoring
- Environmental context and advisory visualization

The 2022 floods in Khairpur District are being used as the primary historical study case.

---

## Development Progress

### ✅ Completed

#### Core Application
- FastAPI backend implemented
- Web dashboard implemented
- SQLite cache and alert functionality
- Historical replay framework
- Open-Meteo integration
- GloFAS integration

#### Software Testing
- Automated backend test suite implemented
- 12/12 automated tests passing
- API functionality tested
- Advisory logic tested
- Historical functionality tested
- Metrics functionality tested

#### Google Earth Engine
- Noncommercial Earth Engine access configured
- Earth Engine project created
- Khairpur District boundary identified
- Administrative boundary verified successfully

#### Sentinel-1 Investigation
- Sentinel-1 GRD dataset connected
- VV and VH polarization availability verified
- Pre-flood imagery identified
- Flood-period imagery identified
- Ascending and descending passes investigated
- Relative orbit numbers investigated

Available relative orbits:

- 5
- 42
- 71
- 78
- 144

Current candidate:

**Relative Orbit 144 — ASCENDING**

Available observations:

- Pre-flood: 15
- Flood-period: 15

---

## 🚧 Currently In Progress

### Sentinel-1 Flood Detection

Current work focuses on:

1. Selecting consistent Sentinel-1 acquisition geometry
2. Comparing pre-flood and flood-period observations
3. Detecting radar backscatter changes
4. Creating an initial flood mask
5. Removing obvious false detections
6. Separating permanent water where appropriate
7. Calculating flood extent within Khairpur District

---

## ⏳ Upcoming Work

### Agricultural Exposure

- Integrate land-cover/cropland information
- Overlay detected flood extent with agricultural areas
- Calculate potentially affected cropland area

### Crop Recovery

- Load Sentinel-2 imagery
- Apply cloud masking
- Calculate NDVI
- Establish vegetation baseline
- Measure post-flood vegetation recovery
- Generate recovery indicators

### Validation

- Compare flood outputs with available reference information
- Evaluate flood-mask quality
- Document limitations
- Record quantitative evaluation metrics where supported

### Final FYP Work

- Complete dashboard integration
- Finalize methodology
- Complete evaluation
- Prepare results
- Finalize thesis documentation
- Prepare presentation/demo

---

## Verified Test Status

```text
12 passed
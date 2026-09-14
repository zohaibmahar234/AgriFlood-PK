# 🌊 AgriFlood-PK

### Flood Detection and Crop Recovery Monitoring in Sindh

**Final Year Project (FYP)** focused on satellite-based flood detection, agricultural exposure assessment, and post-flood crop recovery monitoring in **Khairpur District, Sindh, Pakistan**.

![FYP](https://img.shields.io/badge/Project-Final%20Year%20Project-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Earth Engine](https://img.shields.io/badge/Google-Earth%20Engine-brightgreen)
![Sentinel-1](https://img.shields.io/badge/Satellite-Sentinel--1-orange)
![Sentinel-2](https://img.shields.io/badge/Satellite-Sentinel--2-orange)
![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-success)

---

## 📌 Project Overview

Flooding can cause severe damage to agricultural regions of Sindh, affecting crops, farmland, and rural communities.

**AgriFlood-PK** is an academic geospatial monitoring system designed to investigate how satellite remote sensing and environmental data can be used to:

- Detect flood-affected areas.
- Estimate potentially affected agricultural land.
- Monitor vegetation and crop recovery after flooding.
- Provide weather and river-discharge context.
- Visualize results through an interactive web dashboard.

The initial study area is **Khairpur District, Sindh, Pakistan**, with particular focus on the 2022 flood event.

---

## 🎯 Research Question

> How can satellite remote sensing using Sentinel-1 and Sentinel-2 data be used to assess flood extent, agricultural exposure, and post-flood crop recovery in Khairpur District, Sindh, Pakistan?

---

## 🚨 Problem

Flood assessment in agricultural regions can be difficult when information comes from multiple sources or when field observations are limited.

Optical satellite imagery can also be affected by heavy cloud cover during flood events.

The project therefore investigates a workflow combining radar and optical satellite observations with environmental information to support post-event analysis.

---

## 💡 Proposed Solution

AgriFlood-PK separates the analysis into four major components:

### 1. Flood Detection

**Sentinel-1 SAR** imagery is used for before/after flood analysis.

Radar imagery is particularly useful because it can operate through cloud cover and does not depend on daylight.

### 2. Agricultural Exposure

Detected flood areas can be compared with cropland/land-cover information to estimate potentially affected agricultural areas.

### 3. Crop Recovery Monitoring

**Sentinel-2** imagery can be used to calculate vegetation indicators such as NDVI and examine vegetation recovery after flooding.

### 4. Environmental Context

Weather forecasts and river-discharge information provide additional environmental context while remaining separate from satellite-observed flood products.

---

## 🛰️ Study Area

**Khairpur District, Sindh, Pakistan**

Google Earth Engine administrative-boundary filtering has been configured for the study district.

Current verified study-area result:

```text
Khairpur feature count: 1
```

---

## 🛰️ Satellite Data

### Sentinel-1

Used for:

- SAR-based flood analysis
- Pre-flood observations
- Flood-period observations
- Same-orbit comparison

Initial 2022 data-availability testing identified:

```text
Pre-flood Sentinel-1 observations: 47
Flood-period Sentinel-1 observations: 45

Available passes:
ASCENDING
DESCENDING

Relative orbits:
5, 42, 71, 78, 144
```

A current candidate for consistent comparison is:

```text
Relative Orbit: 144
Pass: ASCENDING
Pre-flood observations: 15
Flood-period observations: 15
```

This is currently being evaluated as part of the flood-mapping methodology.

### Sentinel-2

Planned/under development for:

- NDVI calculation
- Vegetation-condition assessment
- Post-flood crop recovery monitoring

---

## 🧠 System Workflow

```text
                AgriFlood-PK
                     │
        ┌────────────┴────────────┐
        │                         │
   Environmental              Satellite
      Context                   Analysis
        │                         │
 Open-Meteo / GloFAS       Google Earth Engine
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                 Sentinel-1                Sentinel-2
                     │                         │
              Flood Detection             NDVI Analysis
                     │                         │
                     └──────────┬──────────────┘
                                │
                       Agricultural Exposure
                                │
                                ▼
                         Web Dashboard
```

---

## 🛠️ Technology Stack

### Backend

- Python 3.11
- FastAPI
- SQLite
- Pytest

### Geospatial & Remote Sensing

- Google Earth Engine
- Sentinel-1 SAR
- Sentinel-2
- ESA WorldCover
- UNOSAT reference information

### Environmental Data

- Open-Meteo
- GloFAS river-discharge data

### Frontend

- HTML
- CSS
- JavaScript
- Leaflet

The frontend intentionally uses a lightweight architecture without requiring a Node build process.

---

## 🖥️ Dashboard

The web dashboard is designed to present:

- Flood conditions
- Agricultural exposure
- Crop recovery
- Weather information
- River/discharge context
- Historical flood analysis
- Alerts/advisories

### Screenshots

Dashboard and analysis screenshots will be added as the implementation and scientific validation progress.

---

## 🧪 Software Testing

Automated backend tests currently pass:

```text
12 passed
```

Run the test suite with:

```powershell
pytest backend\tests -q
```

Testing covers backend functionality including API behaviour, advisory logic, historical functionality, and metrics.

See:

```text
reports/SOFTWARE_TEST_REPORT.md
reports/RESEARCH_EVALUATION_REPORT.md
```

for documented testing and evaluation information.

---

## 📊 Current Project Status

### Completed / Working

- FastAPI backend
- Interactive dashboard prototype
- SQLite cache/alert support
- Open-Meteo integration
- GloFAS integration
- Historical replay framework
- Automated backend testing
- Google Earth Engine project setup
- Khairpur District boundary verification
- Sentinel-1 data availability analysis
- Sentinel-1 orbit/pass investigation

### In Progress

- Same-orbit Sentinel-1 flood comparison
- 2022 flood-extent extraction
- Flood-mask refinement
- Scientific validation

### Planned

- Cropland exposure calculation
- Sentinel-2 NDVI analysis
- Crop-recovery monitoring
- Final validation
- Final FYP evaluation and documentation

---

## 📁 Repository Structure

```text
AgriFlood-PK/
│
├── backend/           # FastAPI backend and application logic
├── frontend/          # Dashboard interface
├── scripts/           # Data acquisition and analysis scripts
├── data/              # Demo/reference data
├── docs/              # Research and technical documentation
├── reports/           # Testing and evaluation reports
├── README.md
├── .env.example
└── .gitignore
```

---

## ⚙️ Windows Setup

### 1. Clone the repository

```powershell
git clone https://github.com/zohaibmahar234/AgriFlood-PK.git
cd AgriFlood-PK
```

### 2. Create Python environment

```powershell
py -3.11 -m venv .venv
```

### 3. Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r backend\requirements.txt
```

### 5. Create environment file

```powershell
copy .env.example .env
```

Never commit `.env` or private credentials.

### 6. Run automated tests

```powershell
pytest backend\tests -q
```

### 7. Start the application

```powershell
python -m uvicorn backend.app.main:app --reload --port 8000
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🌍 Google Earth Engine

Scientific satellite processing requires access to a registered Google Earth Engine project.

The Earth Engine workflow is being developed for:

```text
Khairpur District
Sindh, Pakistan
```

Primary datasets include Sentinel-1 and Sentinel-2.

Earth Engine credentials and private configuration must **never be committed to this repository**.

---

## ⚠️ Academic & Safety Disclaimer

AgriFlood-PK is an **academic Final Year Project and research prototype**.

It is **not an official flood-warning or emergency-management service**.

Forecast information, satellite-observed water/flood products, agricultural exposure estimates, and vegetation-recovery indicators should be interpreted as separate analytical outputs.

Results should not be used as a substitute for official disaster-management warnings or operational emergency decisions.

---

## 📚 Documentation

Detailed project documentation is available in the `docs/` directory, including:

- Architecture
- Methodology
- Data acquisition
- Data-source inventory
- Feasibility analysis
- Historical demonstration
- Limitations and future work
- Proposal and thesis drafts

---

## 🚧 Development Status

**Status:** Active Development

Current focus:

> Sentinel-1 same-orbit analysis and 2022 flood detection for Khairpur District.

Development history is maintained through Git commits as the FYP progresses.

---

## 👨‍💻 Author

**Zohaib Mahar**

Final Year Project  
Sukkur IBA University

---

## 📌 Project Title

**AgriFlood-PK: Flood Detection and Crop Recovery Monitoring in Sindh**
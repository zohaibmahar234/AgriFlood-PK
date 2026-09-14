# AgriFlood-PK — Development Changelog

This document records major development milestones of the AgriFlood-PK Final Year Project.

The Git commit history remains the primary technical record of repository changes.

---

## September 2026 — Active Development

### Initial FYP Prototype

- Established the AgriFlood-PK project structure.
- Implemented the FastAPI backend.
- Developed the initial web dashboard.
- Added SQLite-based cache and alert functionality.
- Integrated environmental data components.
- Added historical replay functionality.
- Added technical and research documentation.

### Software Testing

- Implemented automated backend tests.
- Verified API functionality.
- Verified advisory logic.
- Verified historical functionality.
- Verified metrics functionality.
- Reached **12/12 passing automated tests**.

### Dashboard Development

- Developed the initial monitoring dashboard.
- Improved the dashboard interface and presentation.
- Added sections for flood monitoring, agricultural exposure,
  crop recovery, weather, river context, and historical analysis.

### Google Earth Engine Setup

- Registered the project for noncommercial academic Earth Engine use.
- Configured the Earth Engine project.
- Verified access to required Earth Engine datasets.
- Identified the Khairpur District administrative boundary.
- Verified a single matching Khairpur District feature.

### Sentinel-1 Data Investigation

- Connected the Sentinel-1 GRD dataset.
- Verified VV and VH polarization availability.
- Defined pre-flood and flood-period windows for the 2022 case study.
- Identified **47 pre-flood observations**.
- Identified **45 flood-period observations**.
- Investigated ascending and descending acquisition passes.
- Identified relative orbits **5, 42, 71, 78, and 144**.

### Orbit Consistency Analysis

Sentinel-1 observations were compared by relative orbit and pass to
reduce inconsistencies caused by mixing acquisition geometries.

**Relative Orbit 144 — ASCENDING** was selected as the current
candidate for further investigation:

- Pre-flood observations: **15**
- Flood-period observations: **15**

---

## Current Development Phase

### Sentinel-1 Flood Mapping

Work currently focuses on:

- Selecting appropriate pre-flood observations.
- Selecting appropriate flood-period observations.
- Creating consistent same-orbit comparisons.
- Measuring radar backscatter change.
- Generating a preliminary flood mask.
- Refining flood detection.
- Separating permanent water where appropriate.
- Estimating flood extent within Khairpur District.

---

## Upcoming Milestones

### Agricultural Exposure Analysis

- Integrate cropland / land-cover data.
- Overlay flood extent with agricultural areas.
- Estimate potentially flood-affected cropland.

### Sentinel-2 Crop Recovery

- Acquire Sentinel-2 observations.
- Apply cloud filtering/masking.
- Calculate NDVI.
- Establish vegetation baseline.
- Measure post-flood vegetation recovery.

### Scientific Validation

- Compare derived flood products with available reference information.
- Evaluate detection performance where suitable reference data exists.
- Document uncertainty and methodological limitations.

### Final FYP Integration

- Integrate validated outputs into the dashboard.
- Complete evaluation.
- Finalize methodology and results.
- Complete thesis documentation.
- Prepare final demonstration and presentation.

---

## Status

**Project:** Active Development  
**Current Phase:** Sentinel-1 Flood Mapping  
**Study Area:** Khairpur District, Sindh, Pakistan
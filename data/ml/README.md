# AgriFlood-PK ML Dataset

## Purpose

This directory stores data used by the experimental agricultural flood-impact ML pipeline.

No synthetic or fabricated ground-truth labels should be presented as observed crop damage.

## Feature Schema

Each sample should contain the following predictor columns:

| Column | Description | Unit |
| --- | --- | --- |
| vh_pre | Sentinel-1 pre-flood VH backscatter | dB |
| vh_flood | Sentinel-1 flood-period VH backscatter | dB |
| vh_change | Change in VH backscatter | dB |
| flood_detected | Experimental flood-candidate indicator | 0 or 1 |
| ndvi_pre | Pre-event Sentinel-2 NDVI | unitless |
| ndvi_post | Post-event Sentinel-2 NDVI | unitless |
| ndvi_change | Change in NDVI | unitless |
| elevation_m | Terrain elevation | metres |
| slope_deg | Terrain slope | degrees |
| rainfall_mm | Rainfall associated with the analysis period | mm |
| cropland | Cropland indicator | 0 or 1 |

## Target

The intended target column is:

impact_class

Proposed classes:

- 0 = Low Potential Impact
- 1 = Moderate Potential Impact
- 2 = Severe Potential Impact

These values define the model output schema only. Training labels must come from a documented independent reference strategy.

## Required Metadata

Where possible, every sample dataset should also preserve:

- sample_id
- latitude
- longitude
- observation date or analysis period
- district
- label_source
- label_method
- source_version or product identifier

Metadata columns are not automatically model predictors.

## Label Provenance

Every labelled sample must have a traceable `label_source` and `label_method`.

The existing UNOSAT metadata file provides historical event context but is not pixel-level crop-damage ground truth.

## Data Splitting

Training and validation samples should be spatially separated where practical.

Randomly splitting neighbouring pixels can produce spatial leakage and unrealistically optimistic accuracy.

## Scientific Status

Until independent validation is completed, model outputs must be described as:

Experimental Potential Agricultural Flood Impact - Validation pending

# ML Label Strategy - AgriFlood-PK

## Objective

The machine-learning component will estimate **Potential Agricultural Flood Impact** for cropland in Khairpur District.

The model output must not be described as confirmed crop damage unless independent field-validated ground-truth data supports that claim.

## Proposed Classes

- 0 - Low Potential Impact
- 1 - Moderate Potential Impact
- 2 - Severe Potential Impact

These class names define the intended prediction categories only. They do not yet define training labels.

## Predictor Features

### Sentinel-1 SAR
- Pre-flood VH backscatter
- Flood-period VH backscatter
- VH backscatter change
- Flood detection indicator

### Sentinel-2
- Pre-event NDVI
- Post-event NDVI
- NDVI change

### Terrain
- Elevation
- Slope

### Hydrometeorology
- Rainfall

### Agriculture
- Cropland mask

## Ground-Truth Rule

Training labels must not be generated solely from arbitrary thresholds applied to the same predictor features used by the model.

Acceptable label/reference sources may include:

1. Field-survey crop-damage observations.
2. Authoritative geospatial agricultural-damage products.
3. Independently interpreted and documented reference samples.
4. Credible external flood/agricultural-impact datasets with suitable spatial and temporal alignment.

## Current UNOSAT Reference

The existing `data/reference/unosat_2022_khairpur.json` contains historical source metadata and event context.

It does not contain a scientific raster or field-validated pixel-level crop-damage ground truth. Therefore, it must not by itself be used to generate Low, Moderate, or Severe ML training labels.

## Validation

When defensible labels become available, evaluation should report appropriate multiclass metrics, including:

- Confusion matrix
- Precision
- Recall
- F1-score
- Class support
- Overall accuracy

Training and validation samples should be spatially separated where practical to reduce spatial leakage.

## Scientific Reporting

Until independent validation is completed, outputs must be reported as:

**Experimental Potential Agricultural Flood Impact**

and accompanied by:

**Validation pending**

The ML output must remain separate from:

- Sentinel-1 observed flood candidates
- Potentially affected cropland
- Sentinel-2 vegetation-change/recovery indicators
- Official flood or agricultural-damage assessments


## External Agricultural-Damage Reference

Official 2022 flood-impact reporting for Khairpur District may be used as an external district-level reference for contextual validation.

PDMA Sindh reported district-level cropped area and affected crop-area statistics for Khairpur during the 2022 flood emergency. These statistics provide useful evidence that substantial agricultural impacts occurred within the district.

However, district-level totals do not identify which individual pixels or ML samples experienced Low, Moderate, or Severe agricultural impact.

Therefore:

- PDMA district totals will not be converted directly into `impact_class` training labels.
- They may be used for district-level contextual comparison and validation.
- Pixel/sample-level training labels require an independent spatial reference or a documented expert/reference-sampling methodology.
- Flood-candidate and non-flood sampling groups remain predictor/sampling information, not agricultural-impact ground truth.

This separation prevents circular labels and unsupported crop-damage claims.
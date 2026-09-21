# ML Ground-Truth Methodology - AgriFlood-PK

## 1. Purpose

This document defines the proposed methodology for creating defensible sample-level reference labels for the experimental AgriFlood-PK agricultural flood-impact model.

The intended ML output classes are:

- `0` - Low Potential Agricultural Impact
- `1` - Moderate Potential Agricultural Impact
- `2` - Severe Potential Agricultural Impact

These classes must not be assigned solely from the same Sentinel-1, Sentinel-2, terrain, or rainfall predictor variables that will later be supplied to the ML model.

The objective is to reduce circular labelling, spatial leakage, and unsupported crop-damage claims.

---

## 2. Current Scientific Status

At the current project stage, sample-level agricultural-impact ground truth has not yet been established.

Available evidence currently includes:

- Sentinel-1 experimental flood-candidate mapping
- Sentinel-2 vegetation-change indicators
- Cropland overlap
- Terrain information
- Historical UNOSAT flood assessments
- PDMA Sindh district-level agricultural-impact statistics

These sources provide valuable event context, but the currently stored references do not independently identify Low, Moderate, or Severe agricultural impact for each ML sample.

Therefore:

**Supervised agricultural-impact model training must not begin until a defensible reference-labelling procedure is completed.**

---

## 3. Reference Evidence Hierarchy

Potential reference evidence should be prioritized approximately as follows.

### Level A - Strong Reference Evidence

Examples:

- Field-survey crop-damage observations
- Georeferenced agricultural damage assessments
- Authoritative spatial crop-loss datasets
- Independently validated damage polygons or sample points

Where spatial and temporal alignment is suitable, these sources may support direct sample-level labels.

### Level B - Interpreted Independent Spatial Evidence

Examples:

- Independently interpreted high-resolution imagery
- Official inundation maps combined with independently interpreted agricultural condition
- Expert-reviewed reference samples
- Independently produced agricultural-impact maps with documented methodology

These sources may support labels when the interpretation procedure, date, spatial scale, and uncertainty are documented.

### Level C - Contextual Evidence

Examples:

- District-level PDMA crop-damage totals
- UNOSAT reports without sample-level agricultural severity information
- Regional flood summaries
- Published event statistics

These sources may support contextual validation but must not automatically become pixel-level ML labels.

---

## 4. Predictor-Label Separation

The following AgriFlood-PK predictor features must not independently define the target label:

- `vh_pre`
- `vh_flood`
- `vh_change`
- `flood_detected`
- `ndvi_pre`
- `ndvi_post`
- `ndvi_change`
- `elevation_m`
- `slope_deg`
- `rainfall_mm`
- `cropland`

For example, a rule such as:

`Severe = flood_detected == 1 AND ndvi_change < threshold`

must not be used as ML ground truth if `flood_detected` and `ndvi_change` are subsequently supplied to the model as predictors.

Doing so would create circular or pseudo-ground-truth labels.

---

## 5. Reference Sample Unit

Each reference sample should represent a documented geographic location within agricultural land in Khairpur District.

Where possible, each sample should preserve:

- `sample_id`
- latitude
- longitude
- district
- event or observation date
- reference-source date
- assigned `impact_class`
- `label_source`
- `label_method`
- `reference_confidence`
- reviewer information
- notes

The geographic support of the reference observation should be compatible with the spatial scale of the extracted predictor features.

---

## 6. Proposed Label Interpretation

The following categories describe the intended semantic meaning of the classes. They are not automatic numerical thresholds.

### Class 0 - Low Potential Impact

Independent reference evidence indicates little or no observable agricultural flood impact at the sample location.

### Class 1 - Moderate Potential Impact

Independent reference evidence indicates noticeable agricultural flood impact, but evidence does not support classification as severe.

### Class 2 - Severe Potential Impact

Independent reference evidence indicates substantial agricultural flood impact at the sample location.

A class should only be assigned when the available independent evidence supports that interpretation.

---

## 7. Uncertain Samples

If available evidence is:

- ambiguous
- spatially misaligned
- temporally inappropriate
- obscured by cloud or image quality
- contradictory
- insufficient to distinguish impact severity

the sample should not be forced into Low, Moderate, or Severe.

Such samples should be marked as uncertain or excluded from supervised training.

This is preferable to introducing unreliable labels.

---

## 8. Reference Confidence

Where reference samples are manually or independently interpreted, a confidence field should be preserved.

Suggested categories:

- `high`
- `medium`
- `low`

Low-confidence samples should be reviewed before model training and may be excluded from the primary training or validation dataset.

Confidence describes confidence in the reference interpretation, not model prediction confidence.

---

## 9. Sampling Design

Reference samples should cover meaningful variation across the study area.

Sampling should consider:

- Flood-affected and non-flood agricultural areas
- Different parts of Khairpur District
- Different vegetation conditions
- Terrain variation where relevant
- Adequate representation of each final impact class

The existing `flood_candidate` and `non_flood` stratified feature groups may help identify locations for review.

However:

**Sampling groups are not agricultural-impact ground-truth labels.**

The artificial balance used for feature coverage must not be interpreted as real-world flood prevalence or impact prevalence.

---

## 10. Spatial Train-Validation Separation

Neighbouring pixels are often highly correlated.

A purely random pixel-level train/test split may therefore place nearly identical neighbouring samples in both training and validation sets and produce unrealistically optimistic performance.

Where practical, AgriFlood-PK should use spatial separation such as:

- Spatial blocks
- Geographic zones
- Separated reference clusters
- Other documented spatial holdout strategies

The validation area must not be used to create or tune training labels.

---

## 11. Model Training Eligibility

Supervised model training may begin only when:

1. A documented independent reference source or interpretation procedure exists.
2. Each training sample has traceable label provenance.
3. Low, Moderate, and Severe have documented semantic definitions.
4. Uncertain samples are handled explicitly.
5. Predictor-derived circular labels have been avoided.
6. Training and validation splitting strategy has been documented.
7. Class counts and class imbalance have been reviewed.

Until these conditions are satisfied, the ML training scripts should remain experimental placeholders.

---

## 12. Evaluation

Once defensible labels are available, evaluation should include:

- Confusion matrix
- Precision
- Recall
- F1-score
- Overall accuracy
- Per-class support

Where class imbalance exists, macro-averaged metrics should also be considered.

Results must identify:

- Reference-data source
- Number of samples
- Class distribution
- Train/validation strategy
- Spatial separation method
- Known limitations

High numerical accuracy alone must not be presented as proof of real-world crop-damage accuracy.

---

## 13. External Contextual Validation

District-level official statistics may be compared with aggregated AgriFlood-PK results as contextual evidence.

For example, PDMA Sindh's Khairpur agricultural-impact statistics may support comparison of the overall event magnitude.

However, agreement with a district-level total does not independently validate individual sample-level severity predictions.

---

## 14. Explainability

After a scientifically defensible model is trained, model interpretation may include:

- Feature importance
- Permutation importance
- Partial dependence where appropriate
- SHAP analysis if added and scientifically justified

Explainability describes how the trained model uses its predictors.

It does not replace independent ground-truth validation.

---

## 15. Reporting Language

Until independent validation is completed, ML outputs should be described as:

**Experimental Potential Agricultural Flood Impact**

and accompanied by:

**Validation pending**

The project must continue to distinguish between:

- Forecast-based risk advisory
- Sentinel-1 flood candidates
- Potentially affected cropland
- Sentinel-2 vegetation change
- ML-estimated agricultural impact
- Official flood or agricultural-damage assessments

---

## 16. Next Research Action

The next scientific task is to identify and assess candidate independent spatial reference sources for Khairpur District during the 2022 flood event.

Only after their spatial coverage, temporal alignment, methodology, licensing, and suitability have been reviewed should a sample-level labelling workflow be implemented.
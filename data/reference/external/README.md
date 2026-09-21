# External Reference Data

This directory is reserved for external geospatial or tabular reference datasets used by the AgriFlood-PK research workflow.

External files must not automatically be treated as scientific ground truth. Their provenance, spatial and temporal coverage, methodology, licensing conditions, and limitations must be reviewed before they are used for model training or validation.

## Required Provenance

For every external dataset, record:

- Dataset or product name
- Source organization
- Original source URL
- Publication or product date
- Acquisition date
- Geographic coverage
- Temporal coverage
- Data format
- Spatial resolution or mapping scale, when available
- Licence or usage terms
- Processing performed after acquisition
- Intended role in AgriFlood-PK
- Known limitations

## Scientific Use

External reference data may be used for:

- Historical flood-event context
- Independent flood-map comparison
- Agricultural-impact contextual validation
- Reference-sample interpretation
- Model validation when scientifically appropriate

Use as supervised ML ground truth requires an independent spatial reference that can support the assigned target class at the location and scale of each sample.

## ML Label Policy

District-level statistics, flood-candidate masks, NDVI changes, or thresholds derived from model predictor features must not automatically be converted into:

- `0 = Low`
- `1 = Moderate`
- `2 = Severe`

agricultural-impact training labels.

This prevents circular labels and unsupported crop-damage claims.

Each labelled sample should preserve, where applicable:

- `label_source`
- `label_method`
- `source_product`
- `source_date`
- `reference_confidence`
- reviewer or interpretation information

## Current Reference Context

The project currently documents:

- UNOSAT 2022 flood assessments for historical flood context.
- PDMA Sindh 2022 district-level agricultural-impact statistics for Khairpur District.

These references provide important external evidence for the 2022 flood event, but the currently stored metadata does not constitute pixel-level Low, Moderate, or Severe agricultural-impact ground truth.

## Storage Policy

Large or licence-restricted external datasets should not automatically be committed to the public Git repository.

When such data are used, preserve their metadata and acquisition instructions so that the research workflow remains traceable and reproducible.

## Current Status

**Sample-level agricultural-impact ground truth: Not yet established.**

Until a defensible spatial reference and labelling methodology are established, the ML component must remain:

**Experimental Potential Agricultural Flood Impact — Validation pending.**
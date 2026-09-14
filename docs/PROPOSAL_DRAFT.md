# Standard Academic Proposal Draft (not university-approved)

## Title
AgriFlood-PK: Flood Risk, Agricultural Exposure and Crop Recovery Monitoring for Sindh

## Problem statement
Flood information, observed inundation, crop exposure and post-flood vegetation recovery are often presented as if they were one prediction problem. This project develops an academic prototype that separates forecast-based advisory from satellite-observed water, potential cropland exposure and vegetation recovery, using Khairpur District as a reproducible case study.

## Objectives
1. Build an interpretable forecast advisory using openly accessible weather/discharge data without presenting it as a calibrated probability.
2. Detect floodwater candidates from consistent Sentinel-1 observations while masking persistent water and common false positives.
3. Estimate potentially affected cropland by spatial overlay.
4. Track post-event NDVI relative to a seasonal baseline with cloud screening.
5. Validate satellite flood detection against time/location-matched credible references and separately test software correctness.

## Research questions
- How accurately can a simple, reproducible Sentinel-1 change baseline identify floodwater in a selected Sindh district relative to a suitable reference?
- How much mapped floodwater overlaps a transparent cropland mask?
- How do cloud-screened vegetation indicators change during post-flood recovery relative to a seasonal baseline?
- What failure modes arise when forecast model data, remote sensing observations and reference products differ in scale and timing?

## ML scope decision
No trained model is claimed in the baseline. If the university requires trained ML, a Random Forest/XGBoost experiment should be added only after acquiring labels that support spatial/temporal holdout and a meaningful comparison with the baseline.

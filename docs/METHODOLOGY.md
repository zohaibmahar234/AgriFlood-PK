# Methodology

## Sentinel-1 baseline
Filter Khairpur; select IW mode, same requested orbit pass and polarization; create pre/post median composites; flag pixels that become sufficiently dark and decrease in backscatter; remove high-occurrence permanent water and slopes above 5°. Thresholds are starting values, not validated constants.

## Exposure
Intersect the detected flood mask with ESA WorldCover class 40. Compute geodesic pixel area. Report **potentially affected cropland**, not destroyed crops or monetary loss.

## Recovery
Use Sentinel-2 Surface Reflectance Harmonized, join Cloud Probability, mask cloudy pixels, compute NDVI, and compare a post-event window with a similar-season baseline. Interpret as vegetation-condition/recovery indication only.

## Validation protocol
Rasterize/reproject prediction and time-matched reference to a common grid. Exclude nodata/unanalysed reference zones. Compute TP/FP/FN/TN, precision, recall, F1 and IoU. Report sensor/date mismatch explicitly. For any future ML, split by held-out area/event rather than random neighbouring pixels to reduce leakage.

## Forecast evaluation
The current advisory is an experimental rule, not a calibrated model. If evaluated later, use archived forecasts initialized before events, report false alarms/misses and true warning lead time, and never use post-event observations as predictive inputs.

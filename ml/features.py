"""Feature schema for AgriFlood-PK agricultural impact modelling.

The features combine satellite, terrain, hydrometeorological, and
agricultural information. They are predictors only and must not be
interpreted individually as confirmed crop damage.
"""

FEATURE_COLUMNS = [
    # Sentinel-1 SAR
    "vh_pre",
    "vh_flood",
    "vh_change",
    "flood_detected",

    # Sentinel-2 vegetation
    "ndvi_pre",
    "ndvi_post",
    "ndvi_change",

    # Terrain
    "elevation_m",
    "slope_deg",

    # Hydrometeorology
    "rainfall_mm",

    # Agricultural mask
    "cropland",
]

TARGET_COLUMN = "impact_class"

IMPACT_CLASSES = {
    0: "Low",
    1: "Moderate",
    2: "Severe",
}


def validate_feature_columns(columns):
    """Return missing model features from a dataset."""
    available = set(columns)
    return [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in available
    ]
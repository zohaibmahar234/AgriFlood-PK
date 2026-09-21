"""Export unlabeled geospatial predictor samples for AgriFlood-PK.

This script builds a feature table for the experimental agricultural
flood-impact ML pipeline. It intentionally does NOT create impact_class
labels. Independent reference labels must be joined later.
"""

import argparse
import os

import ee
import pandas as pd
from dotenv import load_dotenv


DISTRICT_NAME = "Khairpur District"

# Keep these defaults aligned with the verified 2022 prototype.
S1_PRE_START = "2022-05-01"
S1_PRE_END = "2022-07-01"
S1_FLOOD_START = "2022-08-01"
S1_FLOOD_END = "2022-09-30"

S2_PRE_START = "2022-05-01"
S2_PRE_END = "2022-07-01"
S2_POST_START = "2022-10-01"
S2_POST_END = "2022-12-31"

ORBIT_PASS = "ASCENDING"
RELATIVE_ORBIT = 144
CLOUD_PROBABILITY_MAX = 40


def initialize_ee():
    """Initialize Earth Engine using the configured project."""
    load_dotenv()

    project_id = os.getenv("GEE_PROJECT_ID")

    if not project_id:
        raise RuntimeError(
            "GEE_PROJECT_ID is missing. Add it to .env before running."
        )

    ee.Initialize(project=project_id)


def get_study_area():
    """Return Khairpur District geometry."""
    districts = ee.FeatureCollection("FAO/GAUL/2015/level2")

    return (
        districts
        .filter(ee.Filter.eq("ADM0_NAME", "Pakistan"))
        .filter(ee.Filter.eq("ADM2_NAME", DISTRICT_NAME))
        .geometry()
    )


def sentinel1_features(aoi):
    """Build Sentinel-1 flood-related predictor bands."""

    def collection(start, end):
        return (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(aoi)
            .filterDate(start, end)
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .filter(ee.Filter.eq("orbitProperties_pass", ORBIT_PASS))
            .filter(
                ee.Filter.eq(
                    "relativeOrbitNumber_start",
                    RELATIVE_ORBIT,
                )
            )
            .filter(
                ee.Filter.listContains(
                    "transmitterReceiverPolarisation",
                    "VH",
                )
            )
            .select("VH")
        )

    pre = collection(S1_PRE_START, S1_PRE_END)
    flood = collection(S1_FLOOD_START, S1_FLOOD_END)

    pre_count = pre.size().getInfo()
    flood_count = flood.size().getInfo()

    if pre_count == 0 or flood_count == 0:
        raise RuntimeError(
            "Sentinel-1 collection is empty for one or more periods."
        )

    vh_pre = pre.median().rename("vh_pre")
    vh_flood = flood.median().rename("vh_flood")

    vh_change = (
        vh_flood
        .subtract(vh_pre)
        .rename("vh_change")
    )

    candidate = vh_flood.lt(-18).And(
        vh_change.lt(-3)
    )

    permanent_water = (
        ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        .select("occurrence")
        .gte(80)
    )

    elevation = ee.Image("USGS/SRTMGL1_003").select("elevation")

    slope = (
        ee.Terrain.slope(elevation)
        .rename("slope_deg")
    )

    slope_mask = slope.lte(5)

    flood_detected = (
        candidate
        .And(permanent_water.Not())
        .And(slope_mask)
        .rename("flood_detected")
        .unmask(0)
    )

    return (
        vh_pre
        .addBands(vh_flood)
        .addBands(vh_change)
        .addBands(flood_detected)
    )


def sentinel2_features(aoi):
    """Build Sentinel-2 NDVI predictor bands."""

    sentinel2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
    )

    clouds = (
        ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
        .filterBounds(aoi)
    )

    joined = ee.ImageCollection(
        ee.Join.saveFirst("cloud_mask").apply(
            primary=sentinel2,
            secondary=clouds,
            condition=ee.Filter.equals(
                leftField="system:index",
                rightField="system:index",
            ),
        )
    ).filter(
        ee.Filter.notNull(["cloud_mask"])
    )

    def calculate_ndvi(image):
        image = ee.Image(image)

        probability = (
            ee.Image(image.get("cloud_mask"))
            .select("probability")
        )

        masked = image.updateMask(
            probability.lt(CLOUD_PROBABILITY_MAX)
        )

        return (
            masked
            .normalizedDifference(["B8", "B4"])
            .rename("NDVI")
            .copyProperties(
                image,
                ["system:time_start", "system:index"],
            )
        )

    ndvi = joined.map(calculate_ndvi)

    pre = ndvi.filterDate(
        S2_PRE_START,
        S2_PRE_END,
    )

    post = ndvi.filterDate(
        S2_POST_START,
        S2_POST_END,
    )

    pre_count = pre.size().getInfo()
    post_count = post.size().getInfo()

    if pre_count == 0 or post_count == 0:
        raise RuntimeError(
            "Sentinel-2 collection is empty for one or more periods."
        )

    ndvi_pre = pre.median().rename("ndvi_pre")
    ndvi_post = post.median().rename("ndvi_post")

    ndvi_change = (
        ndvi_post
        .subtract(ndvi_pre)
        .rename("ndvi_change")
    )

    return (
        ndvi_pre
        .addBands(ndvi_post)
        .addBands(ndvi_change)
    )


def build_feature_image(aoi):
    """Combine satellite, terrain, and agricultural predictors."""

    s1 = sentinel1_features(aoi)
    s2 = sentinel2_features(aoi)

    elevation = (
        ee.Image("USGS/SRTMGL1_003")
        .select("elevation")
        .rename("elevation_m")
    )

    slope = (
        ee.Terrain.slope(elevation)
        .rename("slope_deg")
    )

    cropland = (
        ee.ImageCollection("ESA/WorldCover/v200")
        .first()
        .select("Map")
        .eq(40)
        .rename("cropland")
    )

    # Samples are restricted to cropland.
    # Therefore cropland is retained for provenance/schema consistency,
    # although it will normally equal 1 in this exported dataset.
    return (
        s1
        .addBands(s2)
        .addBands(elevation)
        .addBands(slope)
        .addBands(cropland)
        .updateMask(cropland)
        .clip(aoi)
    )


def sample_features(feature_image, aoi, sample_count, seed):
    """Generate stratified flood/non-flood cropland samples.

    This sampling is for feature coverage only. The flood/non-flood
    groups are not agricultural-impact ground-truth labels and the
    resulting class balance must not be interpreted as flood prevalence.
    """

    required_bands = [
        "vh_pre",
        "vh_flood",
        "vh_change",
        "flood_detected",
        "ndvi_pre",
        "ndvi_post",
        "ndvi_change",
        "elevation_m",
        "slope_deg",
        "cropland",
    ]

    flood_target = sample_count // 2
    non_flood_target = sample_count - flood_target

    samples = feature_image.stratifiedSample(
        numPoints=0,
        classBand="flood_detected",
        region=aoi,
        scale=20,
        classValues=[0, 1],
        classPoints=[non_flood_target, flood_target],
        seed=seed,
        dropNulls=True,
        tileScale=4,
        geometries=True,
    )

    samples = samples.filter(
        ee.Filter.notNull(required_bands)
    )

    def add_metadata(feature):
        coordinates = feature.geometry().coordinates()

        return feature.set({
            "longitude": coordinates.get(0),
            "latitude": coordinates.get(1),
            "district": DISTRICT_NAME,
            "analysis_year": 2022,
            "sampling_group": ee.Algorithms.If(
                ee.Number(feature.get("flood_detected")).eq(1),
                "flood_candidate",
                "non_flood",
            ),
            "sampling_design": "stratified_feature_coverage",
            "label_source": "unlabeled",
            "label_method": "not_assigned",
        })

    return samples.map(add_metadata)

def to_dataframe(samples):
    """Convert sampled Earth Engine features to a pandas DataFrame."""
    data = samples.getInfo()

    rows = []

    for index, feature in enumerate(data["features"], start=1):
        properties = feature["properties"].copy()
        properties["sample_id"] = f"KHP_{index:05d}"
        rows.append(properties)

    dataframe = pd.DataFrame(rows)

    preferred_columns = [
        "sample_id",
        "latitude",
        "longitude",
        "district",
        "analysis_year",
        "vh_pre",
        "vh_flood",
        "vh_change",
        "flood_detected",
        "ndvi_pre",
        "ndvi_post",
        "ndvi_change",
        "elevation_m",
        "slope_deg",
        "cropland",
        "sampling_group",
        "sampling_design",
        "label_source",
        "label_method",
    ]

    available = [
        column
        for column in preferred_columns
        if column in dataframe.columns
    ]

    return dataframe[available]


def main():
    parser = argparse.ArgumentParser(
        description="Extract unlabeled AgriFlood-PK ML predictor samples."
    )

    parser.add_argument(
        "--samples",
        type=int,
        default=500,
        help="Requested number of cropland samples.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random sampling seed.",
    )

    parser.add_argument(
        "--output",
        default="data/ml/khairpur_features_2022.csv",
        help="Output CSV path.",
    )

    args = parser.parse_args()

    if args.samples <= 0:
        raise ValueError("--samples must be greater than zero.")

    print("Initializing Earth Engine...")
    initialize_ee()

    print("Loading Khairpur District...")
    aoi = get_study_area()

    print("Building predictor image...")
    feature_image = build_feature_image(aoi)

    print(f"Sampling up to {args.samples} cropland locations...")
    samples = sample_features(
        feature_image,
        aoi,
        args.samples,
        args.seed,
    )

    dataframe = to_dataframe(samples)

    if dataframe.empty:
        raise RuntimeError("No valid ML feature samples were returned.")

    os.makedirs(
        os.path.dirname(args.output) or ".",
        exist_ok=True,
    )

    dataframe.to_csv(
        args.output,
        index=False,
    )

    print()
    print("ML FEATURE EXTRACTION: PASS")
    print(f"Rows exported: {len(dataframe)}")
    print(f"Columns exported: {len(dataframe.columns)}")
    print(f"Output: {args.output}")
    print()
    print(
        "NOTE: This dataset is unlabeled. "
        "No impact_class ground truth has been generated."
    )


if __name__ == "__main__":
    main()
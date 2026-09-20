from datetime import datetime, timezone

from .config import settings


def _init():
    """Initialize Google Earth Engine."""
    if not settings.gee_enabled or not settings.gee_project_id:
        raise RuntimeError(
            "Google Earth Engine is not configured. "
            "Set GEE_ENABLED=true and GEE_PROJECT_ID after authentication."
        )

    import ee

    ee.Initialize(project=settings.gee_project_id)
    return ee


def _study_area(ee):
    """Return the Khairpur District boundary."""
    fc = ee.FeatureCollection("FAO/GAUL/2015/level2")

    return fc.filter(
        ee.Filter.And(
            ee.Filter.eq("ADM0_NAME", "Pakistan"),
            ee.Filter.eq("ADM2_NAME", "Khairpur District"),
        )
    ).geometry()


def flood_summary(req):
    """Generate experimental Sentinel-1 flood and crop-exposure summary."""

    ee = _init()
    aoi = _study_area(ee)

    # ---------------------------------------------------------
    # Sentinel-1 collection
    # ---------------------------------------------------------
    def col(start, end):
        return (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(aoi)
            .filterDate(str(start), str(end))
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .filter(
                ee.Filter.eq(
                    "orbitProperties_pass",
                    req.orbit_pass,
                )
            )
            .filter(
                ee.Filter.eq(
                    "relativeOrbitNumber_start",
                    req.relative_orbit,
                )
            )
            .filter(
                ee.Filter.listContains(
                    "transmitterReceiverPolarisation",
                    req.polarization,
                )
            )
            .select(req.polarization)
        )

    # ---------------------------------------------------------
    # Before / flood-period collections
    # ---------------------------------------------------------
    before = col(
        req.before_start,
        req.before_end,
    )

    after = col(
        req.after_start,
        req.after_end,
    )

    before_count = before.size().getInfo()
    after_count = after.size().getInfo()

    if before_count == 0 or after_count == 0:
        return {
            "status": "empty",
            "district": "Khairpur District",
            "before_scenes": before_count,
            "after_scenes": after_count,
            "orbit_pass": req.orbit_pass,
            "relative_orbit": req.relative_orbit,
            "polarization": req.polarization,
        }

    # ---------------------------------------------------------
    # Median Sentinel-1 composites
    # ---------------------------------------------------------
    before_composite = before.median()
    after_composite = after.median()

    # ---------------------------------------------------------
    # Experimental flood-change detection
    # ---------------------------------------------------------
    # Candidate flood pixels must:
    # 1. Be dark in the flood-period SAR composite.
    # 2. Show a significant decrease in backscatter.
    #
    # These thresholds are an experimental baseline and
    # require scientific validation before final claims.

    candidate = after_composite.lt(-18).And(
        after_composite.subtract(before_composite).lt(-3)
    )

    # ---------------------------------------------------------
    # Remove permanent water
    # ---------------------------------------------------------
    permanent_water = (
        ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        .select("occurrence")
        .gte(80)
    )

    # ---------------------------------------------------------
    # Remove steep terrain
    # ---------------------------------------------------------
    elevation = ee.Image("USGS/SRTMGL1_003")

    slope_mask = ee.Terrain.slope(
        elevation
    ).lte(5)

    # ---------------------------------------------------------
    # Final experimental flood mask
    # ---------------------------------------------------------
    flood = (
        candidate
        .And(permanent_water.Not())
        .And(slope_mask)
        .selfMask()
        .clip(aoi)
    )

    # ---------------------------------------------------------
    # Cropland mask — ESA WorldCover
    # Class 40 = Cropland
    # ---------------------------------------------------------
    cropland = (
        ee.ImageCollection("ESA/WorldCover/v200")
        .first()
        .select("Map")
        .eq(40)
        .clip(aoi)
    )

    affected_cropland = (
        flood
        .And(cropland)
        .selfMask()
    )

    # ---------------------------------------------------------
    # Area calculations
    # ---------------------------------------------------------
    pixel_area = ee.Image.pixelArea()

    flood_area = (
        pixel_area
        .updateMask(flood)
        .reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e10,
        )
        .get("area")
    )

    crop_area = (
        pixel_area
        .updateMask(affected_cropland)
        .reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=10,
            maxPixels=1e10,
        )
        .get("area")
    )

    flood_km2 = (
        ee.Number(flood_area)
        .divide(1e6)
        .getInfo()
    )

    crop_km2 = (
        ee.Number(crop_area)
        .divide(1e6)
        .getInfo()
    )
      # ---------------------------------------------------------
# Earth Engine map tiles for flood and cropland exposure
# ---------------------------------------------------------

# Experimental Sentinel-1 flood candidate layer
    flood_map = flood.selfMask().getMapId({
    "palette": ["00FFFF"]
})
    flood_tile_url = flood_map["tile_fetcher"].url_format

# Potentially affected cropland layer
    affected_cropland_map = affected_cropland.selfMask().getMapId({
    "palette": ["FFD54F"]
})
    affected_cropland_tile_url = (
    affected_cropland_map["tile_fetcher"].url_format
    )
    # ---------------------------------------------------------
    # API response
    # ---------------------------------------------------------
    return {
        "status": "ok",
        "district": "Khairpur District",
        "data_source": "Sentinel-1 SAR",
        "polarization": req.polarization,
        "orbit_pass": req.orbit_pass,
        "relative_orbit": req.relative_orbit,
        "before_scenes": before_count,
        "after_scenes": after_count,
        "total_scenes": before_count + after_count,
        "flood_km2": flood_km2,
        "flood_tile_url": flood_tile_url,
        "potentially_affected_cropland_km2": crop_km2,
        "affected_cropland_tile_url": affected_cropland_tile_url,
        "method": (
            "Sentinel-1 backscatter change baseline with "
            "permanent-water and <=5 degree slope filtering"
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "experimental": True,
        "validation_status": "Validation pending",
    }
def recovery_summary(req):
    """Generate Sentinel-2 NDVI crop-recovery summary."""

    ee = _init()
    aoi = _study_area(ee)

    sentinel2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
    )

    clouds = (
        ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
        .filterBounds(aoi)
    )

    join = ee.Join.saveFirst("cloud_mask").apply(
        primary=sentinel2,
        secondary=clouds,
        condition=ee.Filter.equals(
            leftField="system:index",
            rightField="system:index",
        ),
    )

    def ndvi(img):
        cloud_probability = (
            ee.Image(img.get("cloud_mask"))
            .select("probability")
        )

        img = ee.Image(img).updateMask(
            cloud_probability.lt(
                req.cloud_probability_max
            )
        )

        return img.normalizedDifference(
            ["B8", "B4"]
        ).rename("NDVI")

    joined = ee.ImageCollection(join).map(ndvi)

    baseline = joined.filterDate(
        str(req.baseline_start),
        str(req.baseline_end),
    )

    recovery = joined.filterDate(
        str(req.recovery_start),
        str(req.recovery_end),
    )

    baseline_count = baseline.size().getInfo()
    recovery_count = recovery.size().getInfo()

    if baseline_count == 0 or recovery_count == 0:
        return {
            "status": "empty",
            "baseline_scenes": baseline_count,
            "recovery_scenes": recovery_count,
        }

    cropland = (
        ee.ImageCollection("ESA/WorldCover/v200")
        .first()
        .select("Map")
        .eq(40)
    )

    def mean_ndvi(image):
        return (
            ee.Image(image)
            .updateMask(cropland)
            .reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=20,
                maxPixels=1e10,
            )
            .get("NDVI")
        )

    baseline_ndvi = mean_ndvi(
        baseline.median()
    )

    recovery_ndvi = mean_ndvi(
        recovery.median()
    )

    baseline_value = ee.Number(
        baseline_ndvi
    ).getInfo()

    recovery_value = ee.Number(
        recovery_ndvi
    ).getInfo()

    return {
        "status": "ok",
        "district": "Khairpur District",
        "baseline_ndvi": baseline_value,
        "recovery_ndvi": recovery_value,
        "ndvi_change": recovery_value - baseline_value,
        "baseline_scenes": baseline_count,
        "recovery_scenes": recovery_count,
        "data_source": "Sentinel-2",
        "note": (
            "Vegetation recovery indicator only; "
            "not a crop-disease diagnosis."
        ),
    }
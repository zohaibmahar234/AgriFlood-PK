// ============================================================
// AgriFlood-PK
// Sentinel-1 Flood Detection & Agricultural Exposure
// Study Area: Khairpur District, Sindh, Pakistan
// Historical Event: 2022 Flood
// ============================================================


// ------------------------------------------------------------
// 1. STUDY AREA — KHAIRPUR DISTRICT
// ------------------------------------------------------------

var districts = ee.FeatureCollection('FAO/GAUL/2015/level2');

var khairpur = districts
  .filter(ee.Filter.eq('ADM0_NAME', 'Pakistan'))
  .filter(ee.Filter.eq('ADM2_NAME', 'Khairpur District'));

print('Khairpur feature count:', khairpur.size());

Map.centerObject(khairpur, 9);
Map.addLayer(
  khairpur,
  {color: 'yellow'},
  'Khairpur District Boundary'
);


// ------------------------------------------------------------
// 2. SENTINEL-1 BASE COLLECTION
// ------------------------------------------------------------

var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(khairpur)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(
    ee.Filter.listContains(
      'transmitterReceiverPolarisation',
      'VV'
    )
  )
  .filter(
    ee.Filter.listContains(
      'transmitterReceiverPolarisation',
      'VH'
    )
  )

  // Verified during feasibility testing
  .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 144));


// ------------------------------------------------------------
// 3. HISTORICAL WINDOWS
// ------------------------------------------------------------

var preFlood = s1.filterDate(
  '2022-05-01',
  '2022-07-01'
);

var floodPeriod = s1.filterDate(
  '2022-08-01',
  '2022-09-30'
);

print('Selected pre-flood scenes:', preFlood.size());
print('Selected flood-period scenes:', floodPeriod.size());


// ------------------------------------------------------------
// 4. CREATE MEDIAN COMPOSITES
// ------------------------------------------------------------

var preVH = preFlood
  .select('VH')
  .median()
  .clip(khairpur);

var floodVH = floodPeriod
  .select('VH')
  .median()
  .clip(khairpur);

var preVV = preFlood
  .select('VV')
  .median()
  .clip(khairpur);

var floodVV = floodPeriod
  .select('VV')
  .median()
  .clip(khairpur);


// ------------------------------------------------------------
// 5. VISUALIZE SENTINEL-1
// ------------------------------------------------------------

Map.addLayer(
  preVH,
  {min: -25, max: -5},
  'Pre-Flood VH'
);

Map.addLayer(
  floodVH,
  {min: -25, max: -5},
  'Flood-Period VH'
);


// ------------------------------------------------------------
// 6. FLOOD CHANGE DETECTION
// ------------------------------------------------------------

// Difference in VH backscatter.
// Flooded surfaces commonly show reduced radar backscatter,
// but this threshold remains an experimental baseline.

var vhChange = floodVH.subtract(preVH);

var darkWater = floodVH.lt(-18);

var significantDrop = vhChange.lt(-3);

var floodCandidate = darkWater.and(significantDrop);


// ------------------------------------------------------------
// 7. REMOVE PERMANENT WATER
// ------------------------------------------------------------

var permanentWater = ee.Image(
  'JRC/GSW1_4/GlobalSurfaceWater'
)
  .select('occurrence')
  .gte(80);

var noPermanentWater = floodCandidate.and(
  permanentWater.not()
);


// ------------------------------------------------------------
// 8. SLOPE FILTER
// ------------------------------------------------------------

var elevation = ee.Image('USGS/SRTMGL1_003');

var slope = ee.Terrain.slope(elevation);

var lowSlope = slope.lte(5);

var flood = noPermanentWater
  .and(lowSlope)
  .selfMask()
  .clip(khairpur);


// ------------------------------------------------------------
// 9. AGRICULTURAL LAND
// ------------------------------------------------------------

var worldCover = ee.ImageCollection(
  'ESA/WorldCover/v200'
).first();

var cropland = worldCover
  .select('Map')
  .eq(40)
  .clip(khairpur);

var affectedCropland = flood
  .and(cropland)
  .selfMask();


// ------------------------------------------------------------
// 10. MAP RESULTS
// ------------------------------------------------------------

Map.addLayer(
  flood,
  {palette: ['00FFFF']},
  'Experimental Flood Extent'
);

Map.addLayer(
  cropland.selfMask(),
  {palette: ['00AA00']},
  'Cropland',
  false
);

Map.addLayer(
  affectedCropland,
  {palette: ['FF00FF']},
  'Potentially Affected Cropland'
);


// ------------------------------------------------------------
// 11. AREA CALCULATIONS
// ------------------------------------------------------------

var pixelArea = ee.Image.pixelArea();

var floodArea = pixelArea
  .updateMask(flood)
  .reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: khairpur.geometry(),
    scale: 10,
    maxPixels: 1e10
  })
  .getNumber('area')
  .divide(1e6);

var affectedCropArea = pixelArea
  .updateMask(affectedCropland)
  .reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: khairpur.geometry(),
    scale: 10,
    maxPixels: 1e10
  })
  .getNumber('area')
  .divide(1e6);


// ------------------------------------------------------------
// 12. OUTPUT
// ------------------------------------------------------------

print('Flood extent (km²):', floodArea);

print(
  'Potentially affected cropland (km²):',
  affectedCropArea
);

print(
  'IMPORTANT:',
  'Flood thresholds are an experimental baseline and require validation before scientific claims.'
);
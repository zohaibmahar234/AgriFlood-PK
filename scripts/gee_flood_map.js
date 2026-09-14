// AgriFlood-PK feasibility script — paste into the Google Earth Engine Code Editor.
// Requires a registered/verified noncommercial Earth Engine project.
var studyArea = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM0_NAME','Pakistan')).filter(ee.Filter.eq('ADM2_NAME','Khairpur'));
Map.centerObject(studyArea, 8); Map.addLayer(studyArea, {color:'yellow'}, 'Khairpur District boundary');
function s1(start,end){return ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(studyArea)
  .filterDate(start,end).filter(ee.Filter.eq('instrumentMode','IW'))
  .filter(ee.Filter.eq('orbitProperties_pass','DESCENDING'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation','VH')).select('VH');}
var before=s1('2022-06-01','2022-07-15'), after=s1('2022-08-25','2022-09-03');
print('Before scenes',before.size(),'After scenes',after.size());
var b=before.median(), a=after.median();
var candidate=a.lt(-18).and(a.subtract(b).lt(-3));
var perm=ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').gte(80);
var slope=ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003')).lte(5);
var flood=candidate.and(perm.not()).and(slope).selfMask().clip(studyArea);
var crop=ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').eq(40);
var cropFlood=flood.and(crop).selfMask();
Map.addLayer(b,{min:-25,max:0},'Before VH'); Map.addLayer(a,{min:-25,max:0},'After VH');
Map.addLayer(flood,{palette:['00FFFF']},'Experimental flood candidate');
Map.addLayer(cropFlood,{palette:['FF00FF']},'Potentially affected cropland');
var area=ee.Image.pixelArea();
print('Flood candidate km2', area.updateMask(flood).reduceRegion({reducer:ee.Reducer.sum(),geometry:studyArea,scale:10,maxPixels:1e10}).getNumber('area').divide(1e6));
print('Potentially affected cropland km2', area.updateMask(cropFlood).reduceRegion({reducer:ee.Reducer.sum(),geometry:studyArea,scale:10,maxPixels:1e10}).getNumber('area').divide(1e6));
// IMPORTANT: thresholds are an unvalidated baseline; tune/validate against time-matched reference before scientific claims.

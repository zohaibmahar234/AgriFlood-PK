from datetime import datetime, timezone
from .config import settings

def _init():
    if not settings.gee_enabled or not settings.gee_project_id:
        raise RuntimeError('Google Earth Engine is not configured. Set GEE_ENABLED=true and GEE_PROJECT_ID after authentication.')
    import ee
    ee.Initialize(project=settings.gee_project_id)
    return ee

def _study_area(ee):
    fc=ee.FeatureCollection('FAO/GAUL/2015/level2')
    return fc.filter(ee.Filter.And(ee.Filter.eq('ADM0_NAME','Pakistan'), ee.Filter.eq('ADM2_NAME','Khairpur'))).geometry()

def flood_summary(req):
    ee=_init(); aoi=_study_area(ee)
    def col(start,end):
        return (ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(aoi).filterDate(str(start),str(end))
          .filter(ee.Filter.eq('instrumentMode','IW')).filter(ee.Filter.eq('orbitProperties_pass', req.orbit_pass))
          .filter(ee.Filter.listContains('transmitterReceiverPolarisation',req.polarization)).select(req.polarization))
    before=col(req.before_start,req.before_end); after=col(req.after_start,req.after_end)
    bc=before.size().getInfo(); ac=after.size().getInfo()
    if bc==0 or ac==0: return {'status':'empty','before_scenes':bc,'after_scenes':ac}
    b=before.median(); a=after.median()
    # Interpretable change baseline: dark after-image and strong backscatter decrease.
    candidate=a.lt(-18).And(a.subtract(b).lt(-3))
    permanent=ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').gte(80)
    slope=ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003')).lte(5)
    flood=candidate.And(permanent.Not()).And(slope).selfMask().clip(aoi)
    crop=ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').eq(40)
    crop_flood=flood.And(crop)
    px=ee.Image.pixelArea()
    flood_km2=px.updateMask(flood).reduceRegion(ee.Reducer.sum(),aoi,10,maxPixels=1e10).get('area')
    crop_km2=px.updateMask(crop_flood).reduceRegion(ee.Reducer.sum(),aoi,10,maxPixels=1e10).get('area')
    return {'status':'ok','district':'Khairpur','method':'Sentinel-1 VH/VV change baseline; permanent-water and <=5° slope masks',
      'before_scenes':bc,'after_scenes':ac,'flood_km2':ee.Number(flood_km2).divide(1e6).getInfo(),
      'potentially_affected_cropland_km2':ee.Number(crop_km2).divide(1e6).getInfo(),
      'generated_at':datetime.now(timezone.utc).isoformat(), 'experimental':True}

def recovery_summary(req):
    ee=_init(); aoi=_study_area(ee)
    s2=ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi)
    clouds=ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY').filterBounds(aoi)
    join=ee.Join.saveFirst('cloud_mask').apply(primary=s2, secondary=clouds,
        condition=ee.Filter.equals(leftField='system:index',rightField='system:index'))
    def ndvi(img):
        cp=ee.Image(img.get('cloud_mask')).select('probability')
        img=ee.Image(img).updateMask(cp.lt(req.cloud_probability_max))
        return img.normalizedDifference(['B8','B4']).rename('NDVI')
    j=ee.ImageCollection(join).map(ndvi)
    base=j.filterDate(str(req.baseline_start),str(req.baseline_end)); rec=j.filterDate(str(req.recovery_start),str(req.recovery_end))
    bc=base.size().getInfo(); rc=rec.size().getInfo()
    if bc==0 or rc==0: return {'status':'empty','baseline_scenes':bc,'recovery_scenes':rc}
    crop=ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').eq(40)
    def mean(im): return ee.Image(im).updateMask(crop).reduceRegion(ee.Reducer.mean(),aoi,20,maxPixels=1e10).get('NDVI')
    b=mean(base.median()); r=mean(rec.median())
    bv=ee.Number(b).getInfo(); rv=ee.Number(r).getInfo()
    return {'status':'ok','baseline_ndvi':bv,'recovery_ndvi':rv,'ndvi_change':rv-bv,
            'baseline_scenes':bc,'recovery_scenes':rc,'note':'Vegetation indicator only; not crop-disease diagnosis.'}

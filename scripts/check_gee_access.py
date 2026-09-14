import os, sys
try:
    import ee
except ImportError:
    sys.exit('earthengine-api is not installed. Run: pip install -r backend/requirements.txt')
project=os.getenv('GEE_PROJECT_ID','').strip()
if not project: sys.exit('Set GEE_PROJECT_ID in your environment/.env first.')
try:
    ee.Initialize(project=project)
    n=(ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(ee.Geometry.Point([67.78,26.73]))
       .filterDate('2022-08-25','2022-09-03').size().getInfo())
    print(f"GEE access OK. Sentinel-1 scenes intersecting the Khairpur Mir's test point/window: {n}")
except Exception as e:
    print('GEE initialization/access failed:',type(e).__name__,str(e))
    print('Authenticate with: earthengine authenticate')
    raise SystemExit(2)

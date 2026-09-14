from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import AdvisoryRequest, AdvisoryResponse, AlertCreate, FloodJobRequest, RecoveryJobRequest
from .advisory import calculate_advisory
from .open_meteo import weather, discharge
from .alerts import init_db, upsert_alert, list_alerts
from . import gee

app=FastAPI(title='AgriFlood-PK API',version='0.1.0')

@app.middleware('http')
async def disable_static_cache(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith('/static/') or request.url.path == '/':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
init_db()
ROOT=Path(__file__).resolve().parents[2]
FRONTEND=ROOT/'frontend'
app.mount('/static',StaticFiles(directory=FRONTEND),name='static')

@app.get('/')
def home(): return FileResponse(FRONTEND/'index.html')

@app.get('/api/health')
def health():
    return {'status':'ok','gee_configured':bool(settings.gee_enabled and settings.gee_project_id),
            'warning':'Academic prototype; not an official flood warning service.'}

@app.post('/api/advisory',response_model=AdvisoryResponse)
def advisory(req:AdvisoryRequest): return calculate_advisory(req)

@app.get('/api/weather')
async def api_weather(lat:float=27.53,lon:float=68.76):
    try: return await weather(lat,lon)
    except Exception as e: raise HTTPException(502,f'Weather provider failed: {type(e).__name__}')

@app.get('/api/discharge')
async def api_discharge(lat:float=27.53,lon:float=68.76):
    try: return await discharge(lat,lon)
    except Exception as e: raise HTTPException(502,f'Flood/discharge provider failed: {type(e).__name__}')

@app.post('/api/alerts')
def create_alert(a:AlertCreate): return upsert_alert(a)
@app.get('/api/alerts')
def get_alerts(): return list_alerts()

@app.post('/api/jobs/flood')
def flood_job(req:FloodJobRequest):
    try: return gee.flood_summary(req)
    except RuntimeError as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(500,f'GEE flood job failed: {type(e).__name__}: {e}')

@app.post('/api/jobs/recovery')
def recovery_job(req:RecoveryJobRequest):
    try: return gee.recovery_summary(req)
    except RuntimeError as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(500,f'GEE recovery job failed: {type(e).__name__}: {e}')

@app.get('/api/historical-replay')
def replay():
    p=ROOT/'data'/'reference'/'unosat_2022_khairpur.json'
    import json
    return json.loads(p.read_text(encoding='utf-8'))

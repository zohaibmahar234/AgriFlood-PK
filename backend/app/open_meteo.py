import httpx
from datetime import datetime, timezone
from .config import settings

WEATHER='https://api.open-meteo.com/v1/forecast'
FLOOD='https://flood-api.open-meteo.com/v1/flood'

async def weather(lat: float, lon: float):
    params={'latitude':lat,'longitude':lon,'current':'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m','hourly':'precipitation','daily':'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum','forecast_days':5,'timezone':'Asia/Karachi'}
    async with httpx.AsyncClient(timeout=settings.open_meteo_timeout_seconds) as c:
        r=await c.get(WEATHER,params=params); r.raise_for_status(); data=r.json()
    vals=data.get('hourly',{}).get('precipitation',[])
    vals=[float(v or 0) for v in vals]
    return {'source':'Open-Meteo','retrieved_at':datetime.now(timezone.utc).isoformat(),
            'rainfall_24h_mm':round(sum(vals[:24]),2) if vals else None,
            'rainfall_72h_mm':round(sum(vals[:72]),2) if vals else None,
            'raw':data}

async def discharge(lat: float, lon: float):
    params={'latitude':lat,'longitude':lon,'daily':'river_discharge','forecast_days':7}
    async with httpx.AsyncClient(timeout=settings.open_meteo_timeout_seconds) as c:
        r=await c.get(FLOOD,params=params); r.raise_for_status(); data=r.json()
    vals=data.get('daily',{}).get('river_discharge',[])
    return {'source':'Open-Meteo/GloFAS','retrieved_at':datetime.now(timezone.utc).isoformat(),
            'river_discharge_m3s': vals[0] if vals else None, 'daily':data.get('daily',{})}

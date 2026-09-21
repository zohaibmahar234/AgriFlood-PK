import os, tempfile
os.environ['DATABASE_URL']='sqlite:///' + tempfile.mktemp(suffix='.db')
from fastapi.testclient import TestClient
from backend.app.main import app
client=TestClient(app)

def test_health():
    r=client.get('/api/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_validation():
    r=client.post('/api/advisory',json={'latitude':999,'longitude':67}); assert r.status_code==422

def test_alert_upsert_prevents_duplicate_key():
    p={'key':'khairpur-demo','state':'Medium','location':'Khairpur','reason':'test','source_date':'2022-08-31','quality':'synthetic software test','simulated':True}
    a=client.post('/api/alerts',json=p); b=client.post('/api/alerts',json={**p,'state':'High'})
    assert a.status_code==200 and b.status_code==200
    rows=client.get('/api/alerts').json(); assert len([x for x in rows if x['key']=='khairpur-demo'])==1

def test_gee_blocker_is_explicit(monkeypatch):
    from backend.app.config import settings

    monkeypatch.setattr(settings, "gee_enabled", False)

    p = {
        "district": "Khairpur",
        "before_start": "2022-06-01",
        "before_end": "2022-07-15",
        "after_start": "2022-08-25",
        "after_end": "2022-09-03",
    }

    r = client.post("/api/jobs/flood", json=p)

    assert r.status_code == 503
    assert "not configured" in r.text

def test_frontend_is_served():
    r=client.get('/')
    assert r.status_code==200 and 'AgriFlood-PK' in r.text
    assert client.get('/static/app.js').status_code==200

def test_expired_alert_is_marked_inactive():
    p={'key':'expired-demo','state':'Medium','location':'Khairpur','reason':'test expiry','source_date':'2022-08-31','quality':'synthetic software test','simulated':True,'expires_at':'2020-01-01T00:00:00+00:00'}
    assert client.post('/api/alerts',json=p).status_code==200
    rows=client.get('/api/alerts').json()
    row=next(x for x in rows if x['key']=='expired-demo')
    assert row['active']==0

def test_provider_failure_returns_502(monkeypatch):
    async def fail(*args,**kwargs): raise RuntimeError('offline')
    monkeypatch.setattr('backend.app.main.weather',fail)
    r=client.get('/api/weather')
    assert r.status_code==502

from fastapi.testclient import TestClient
from backend.app.main import app

def test_historical_replay_is_real_reference_metadata_not_synthetic_claim():
    d=TestClient(app).get('/api/historical-replay').json()
    assert d['mode']=='historical_reference'
    assert d['scientific_raster_included'] is False
    assert 'UNOSAT' in d['sources'][0]['name']

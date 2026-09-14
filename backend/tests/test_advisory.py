from backend.app.advisory import calculate_advisory
from backend.app.models import AdvisoryRequest

def test_unknown_when_most_data_missing():
    r=calculate_advisory(AdvisoryRequest(rainfall_24h_mm=None,rainfall_72h_mm=None,discharge_m3s=10,discharge_baseline_m3s=None))
    assert r.state=='Unknown/Insufficient Data' and r.score is None

def test_high_rule_is_experimental_not_probability():
    r=calculate_advisory(AdvisoryRequest(rainfall_24h_mm=60,rainfall_72h_mm=130,discharge_m3s=250,discharge_baseline_m3s=100))
    assert r.state=='High' and r.experimental is True and r.probability is None

def test_low_does_not_claim_safety():
    r=calculate_advisory(AdvisoryRequest(rainfall_24h_mm=0,rainfall_72h_mm=0,discharge_m3s=50,discharge_baseline_m3s=100))
    assert r.state=='Low'

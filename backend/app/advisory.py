from datetime import datetime, timezone
from .models import AdvisoryRequest, AdvisoryResponse

def calculate_advisory(req: AdvisoryRequest) -> AdvisoryResponse:
    # Deliberately an interpretable baseline, NOT a trained model or calibrated probability.
    missing = []
    if req.rainfall_24h_mm is None: missing.append('24h rainfall')
    if req.rainfall_72h_mm is None: missing.append('72h rainfall')
    if req.discharge_m3s is None or req.discharge_baseline_m3s is None: missing.append('river discharge/baseline')
    if len(missing) >= 2:
        return AdvisoryResponse(state='Unknown/Insufficient Data', score=None,
            reasons=['Missing: ' + ', '.join(missing), 'Missing/stale data is not treated as safety.'],
            generated_at=datetime.now(timezone.utc), input_quality='insufficient')

    score = 0; reasons=[]
    if req.rainfall_24h_mm is not None:
        if req.rainfall_24h_mm >= 50: score += 2; reasons.append('Heavy 24h rainfall signal (>=50 mm).')
        elif req.rainfall_24h_mm >= 25: score += 1; reasons.append('Elevated 24h rainfall signal (>=25 mm).')
    if req.rainfall_72h_mm is not None:
        if req.rainfall_72h_mm >= 100: score += 2; reasons.append('Very high 72h accumulated rainfall signal (>=100 mm).')
        elif req.rainfall_72h_mm >= 60: score += 1; reasons.append('High 72h accumulated rainfall signal (>=60 mm).')
    if req.discharge_m3s is not None and req.discharge_baseline_m3s:
        ratio=req.discharge_m3s/req.discharge_baseline_m3s
        if ratio >= 2.0: score += 3; reasons.append('River discharge is at least 2x the supplied baseline.')
        elif ratio >= 1.4: score += 2; reasons.append('River discharge is at least 1.4x the supplied baseline.')
        elif ratio >= 1.15: score += 1; reasons.append('River discharge is moderately above the supplied baseline.')
    if score >= 5: state='High'
    elif score >= 2: state='Medium'
    else: state='Low'
    if not reasons: reasons=['No experimental trigger crossed; this is not proof of safety.']
    quality='complete' if not missing else 'partial: ' + ', '.join(missing)
    return AdvisoryResponse(state=state, score=score, reasons=reasons,
        generated_at=datetime.now(timezone.utc), input_quality=quality)

from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Literal, Optional

RiskState = Literal['Low','Medium','High','Unknown/Insufficient Data']

class Location(BaseModel):
    name: str = "Khairpur Mir's, Sindh"
    latitude: float = Field(27.53, ge=-90, le=90)
    longitude: float = Field(68.76, ge=-180, le=180)

class AdvisoryRequest(Location):
    rainfall_24h_mm: Optional[float] = Field(default=None, ge=0)
    rainfall_72h_mm: Optional[float] = Field(default=None, ge=0)
    discharge_m3s: Optional[float] = Field(default=None, ge=0)
    discharge_baseline_m3s: Optional[float] = Field(default=None, gt=0)
    data_timestamp: Optional[datetime] = None

class AdvisoryResponse(BaseModel):
    state: RiskState
    score: Optional[int]
    reasons: list[str]
    experimental: bool = True
    probability: None = None
    generated_at: datetime
    input_quality: str

class AlertCreate(BaseModel):
    key: str
    state: RiskState
    location: str
    reason: str
    source_date: str
    quality: str
    expires_at: Optional[datetime] = None
    simulated: bool = False

class AlertOut(AlertCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    active: bool

class FloodJobRequest(BaseModel):
    district: str = 'Khairpur District'
    before_start: date
    before_end: date
    after_start: date
    after_end: date
    orbit_pass: Literal['ASCENDING', 'DESCENDING'] = 'ASCENDING'
    relative_orbit: int = 144
    polarization: Literal['VV', 'VH'] = 'VH'

class RecoveryJobRequest(BaseModel):
    district: str = 'Khairpur'
    baseline_start: date
    baseline_end: date
    recovery_start: date
    recovery_end: date
    cloud_probability_max: int = Field(40, ge=0, le=100)

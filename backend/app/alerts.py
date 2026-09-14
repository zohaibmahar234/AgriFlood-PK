from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from .config import settings

engine=create_engine(settings.database_url, future=True)

def init_db():
    with engine.begin() as c:
        c.execute(text('''CREATE TABLE IF NOT EXISTS alerts (
          id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT UNIQUE NOT NULL, state TEXT NOT NULL,
          location TEXT NOT NULL, reason TEXT NOT NULL, source_date TEXT NOT NULL, quality TEXT NOT NULL,
          expires_at TEXT, simulated INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1)'''))

def upsert_alert(a):
    now=datetime.now(timezone.utc).isoformat()
    with engine.begin() as c:
        row=c.execute(text('SELECT id FROM alerts WHERE key=:k'),{'k':a.key}).fetchone()
        if row:
            c.execute(text('''UPDATE alerts SET state=:state, location=:location, reason=:reason,
                source_date=:source_date, quality=:quality, expires_at=:expires_at, simulated=:simulated,
                updated_at=:updated_at, active=1 WHERE key=:key'''),
                {**a.model_dump(), 'expires_at':a.expires_at.isoformat() if a.expires_at else None,
                 'simulated':int(a.simulated),'updated_at':now})
            aid=row[0]
        else:
            cur=c.execute(text('''INSERT INTO alerts(key,state,location,reason,source_date,quality,expires_at,simulated,created_at,updated_at,active)
                VALUES(:key,:state,:location,:reason,:source_date,:quality,:expires_at,:simulated,:created_at,:updated_at,1)'''),
                {**a.model_dump(),'expires_at':a.expires_at.isoformat() if a.expires_at else None,
                 'simulated':int(a.simulated),'created_at':now,'updated_at':now})
            aid=cur.lastrowid
    return get_alert(aid)

def get_alert(aid):
    with engine.connect() as c:
        r=c.execute(text('SELECT * FROM alerts WHERE id=:i'),{'i':aid}).mappings().fetchone()
    return dict(r) if r else None

def list_alerts():
    now=datetime.now(timezone.utc)
    with engine.begin() as c:
        rows=c.execute(text('SELECT * FROM alerts ORDER BY updated_at DESC')).mappings().all()
        for r in rows:
            exp=r['expires_at']
            if exp:
                try:
                    if datetime.fromisoformat(exp) < now and r['active']:
                        c.execute(text('UPDATE alerts SET active=0 WHERE id=:i'),{'i':r['id']})
                except ValueError: pass
    with engine.connect() as c:
        return [dict(x) for x in c.execute(text('SELECT * FROM alerts ORDER BY updated_at DESC')).mappings().all()]

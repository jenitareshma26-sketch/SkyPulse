from __future__ import annotations
from database.database import Database
class HistoryRepository:
    def __init__(self, db: Database): self.db=db
    def add(self,name,lat,lon):
        with self.db.connection() as c: c.execute("INSERT INTO searches(name,latitude,longitude,used_at) VALUES(?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(name) DO UPDATE SET used_at=CURRENT_TIMESTAMP",(name,lat,lon))
    def recent(self):
        with self.db.connection() as c: return c.execute("SELECT name,latitude,longitude FROM searches ORDER BY used_at DESC LIMIT 8").fetchall()

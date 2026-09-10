from __future__ import annotations
from database.database import Database
class FavoritesRepository:
    def __init__(self, db: Database): self.db=db
    def all(self):
        with self.db.connection() as c: return c.execute("SELECT name,latitude,longitude FROM favorites ORDER BY name").fetchall()
    def toggle(self,name,lat,lon):
        with self.db.connection() as c:
            exists=c.execute("SELECT 1 FROM favorites WHERE name=?",(name,)).fetchone()
            c.execute("DELETE FROM favorites WHERE name=?" if exists else "INSERT INTO favorites(name,latitude,longitude) VALUES(?,?,?)", (name,) if exists else (name,lat,lon))
            return not bool(exists)


"""SQLite persistence with parameterized queries and thread-safe short sessions."""
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH
class Database:
    def __init__(self, path=DATABASE_PATH): self.path = path; self._setup()
    @contextmanager
    def connection(self):
        con = sqlite3.connect(self.path)
        try: yield con; con.commit()
        finally: con.close()
    def _setup(self):
        with self.connection() as con:
            con.executescript('''CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, name TEXT UNIQUE, latitude REAL, longitude REAL, used_at TEXT DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY, name TEXT UNIQUE, latitude REAL, longitude REAL);
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE IF NOT EXISTS weather_cache (location TEXT PRIMARY KEY, payload TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
    def setting(self, key: str, default: str = "") -> str:
        with self.connection() as con:
            row=con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone(); return row[0] if row else default
    def set_setting(self, key: str, value: str):
        with self.connection() as con: con.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key,value))


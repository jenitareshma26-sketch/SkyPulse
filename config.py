"""Application configuration loaded once at startup."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
APP_NAME = "SkyPulse Pro"
DATABASE_PATH = ROOT / "skypulse.db"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
REQUEST_TIMEOUT = 10
CACHE_TTL_SECONDS = 900


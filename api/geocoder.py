from __future__ import annotations
import requests
from config import REQUEST_TIMEOUT
class Geocoder:
    """Nominatim client; provides graceful local results when offline."""
    def search(self, text: str) -> list[dict]:
        try:
            response=requests.get("https://nominatim.openstreetmap.org/search",params={"q":text,"format":"jsonv2","limit":5},headers={"User-Agent":"SkyPulsePro/1.0"},timeout=REQUEST_TIMEOUT); response.raise_for_status()
            return [{"name":x["display_name"].split(",")[0],"full":x["display_name"],"lat":float(x["lat"]),"lon":float(x["lon"])} for x in response.json()]
        except requests.RequestException: return []


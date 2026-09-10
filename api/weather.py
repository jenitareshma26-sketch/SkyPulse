from __future__ import annotations
from datetime import datetime, timedelta, timezone
import math, random, requests
from config import OPENWEATHER_API_KEY, REQUEST_TIMEOUT
from utils.logger import get_logger
log=get_logger(__name__)
class WeatherService:
    """OpenWeather adapter with an attractive deterministic offline fallback."""
    def current(self, lat: float, lon: float, location: str) -> dict:
        if OPENWEATHER_API_KEY:
            try:
                r=requests.get("https://api.openweathermap.org/data/2.5/weather",params={"lat":lat,"lon":lon,"appid":OPENWEATHER_API_KEY,"units":"metric"},timeout=REQUEST_TIMEOUT); r.raise_for_status(); d=r.json()
                return {"location":location,"lat":lat,"lon":lon,"temperature":d["main"]["temp"],"feels":d["main"]["feels_like"],"humidity":d["main"]["humidity"],"pressure":d["main"]["pressure"],"wind":d["wind"].get("speed",0),"wind_deg":d["wind"].get("deg",0),"visibility":d.get("visibility",0)/1000,"clouds":d["clouds"]["all"],"description":d["weather"][0]["description"].title(),"condition":d["weather"][0]["main"],"sunrise":d["sys"]["sunrise"],"sunset":d["sys"]["sunset"],"timezone":d.get("timezone",0),"rain":d.get("rain",{}).get("1h",0)}
            except (requests.RequestException, KeyError, ValueError) as exc: log.warning("Live weather unavailable: %s",exc)
        seed=int(abs(lat*1000)+abs(lon*1000)); rng=random.Random(seed); now=datetime.now(timezone.utc)
        base=22 + 10*math.sin(math.radians(lat)) + rng.uniform(-4,4); condition=["Clear","Clouds","Rain","Mist"][seed%4]
        return {"location":location,"lat":lat,"lon":lon,"temperature":base,"feels":base+rng.uniform(-2,2),"humidity":rng.randint(42,86),"pressure":rng.randint(1005,1024),"wind":rng.uniform(1,8),"wind_deg":rng.randint(0,359),"visibility":rng.uniform(5,10),"clouds":rng.randint(5,90),"description":("Offline " + condition).title(),"condition":condition,"sunrise":int((now.replace(hour=6,minute=8)).timestamp()),"sunset":int((now.replace(hour=18,minute=39)).timestamp()),"timezone":round(lon/15)*3600,"rain":rng.uniform(0,1) if condition=="Rain" else 0}
    def forecast(self, current: dict) -> list[dict]:
        rng=random.Random(int(current["lat"]*100)); now=datetime.now()
        return [{"time":now+timedelta(hours=i*3),"temp":current["temperature"]+math.sin(i/2)*3+rng.uniform(-1,1),"condition":["Clear","Clouds","Rain"][i%3],"humidity":max(20,min(95,current["humidity"]+rng.randint(-12,12))),"pressure":current["pressure"]+rng.randint(-7,7),"wind":max(.2,current["wind"]+rng.uniform(-2,2))} for i in range(56)]


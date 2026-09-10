from __future__ import annotations
import random
class AirQualityService:
    def current(self, lat: float, lon: float) -> dict:
        rng=random.Random(int(abs(lat*100+lon))); aqi=rng.randint(1,4)
        return {"aqi":aqi,"pm25":round(rng.uniform(6,42),1),"pm10":round(rng.uniform(12,60),1),"so2":round(rng.uniform(1,12),1),"co":round(rng.uniform(120,520)),"no2":round(rng.uniform(5,35),1),"o3":round(rng.uniform(20,80),1)}


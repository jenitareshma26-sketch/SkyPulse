from __future__ import annotations
class AlertService:
    def alerts(self, weather: dict) -> list[tuple[str,str]]:
        alerts=[]
        if weather["rain"]>0: alerts.append(("Rain advisory","Bring an umbrella; precipitation is possible today."))
        if weather["temperature"]>=34: alerts.append(("Heat advisory","Stay hydrated and limit strenuous activity at midday."))
        if not alerts: alerts.append(("Conditions stable","No weather alerts are active for this location."))
        return alerts

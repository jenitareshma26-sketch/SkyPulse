from __future__ import annotations
from datetime import datetime
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QFrame
from components.weather_card import WeatherCard
from components.forecast_card import ForecastCard
from components.air_quality_card import AirQualityCard
from components.chart_card import ChartCard
from components.temperature_gauge import TemperatureGauge
from components.weather_icon import WeatherIcon
from utils.units import celsius,wind,pressure
class Dashboard(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent);root=QVBoxLayout(self);root.setContentsMargins(26,8,26,28);root.setSpacing(16);heading=QLabel("Today’s atmosphere");heading.setObjectName("pageTitle");root.addWidget(heading)
        hero=QFrame();hero.setObjectName("hero");h=QHBoxLayout(hero);h.setContentsMargins(30,24,30,22);left=QVBoxLayout();self.place=QLabel();self.place.setObjectName("heroPlace");self.condition=QLabel();self.condition.setObjectName("heroSub");self.temp=QLabel();self.temp.setObjectName("heroTemp");self.feels=QLabel();self.feels.setObjectName("heroSub");left.addWidget(self.place);left.addWidget(self.condition);left.addWidget(self.temp);left.addWidget(self.feels);h.addLayout(left);h.addStretch();self.icon=WeatherIcon("Clear",150);h.addWidget(self.icon);root.addWidget(hero)
        grid=QGridLayout();grid.setHorizontalSpacing(14);grid.setVerticalSpacing(14);self.cards={};specs=[("Feels like","feels","⌁"),("Humidity","humidity","♒"),("Wind","wind","↗"),("Pressure","pressure","◌"),("Visibility","visibility","◉"),("Cloud cover","clouds","☁"),("UV index","uv","☀"),("Rain chance","rain","☂")]
        for i,(title,key,symbol) in enumerate(specs):self.cards[key]=WeatherCard(title,"—",symbol=symbol);grid.addWidget(self.cards[key],i//4,i%4)
        root.addLayout(grid);row=QHBoxLayout();row.setSpacing(14);self.aqi=AirQualityCard();self.chart=ChartCard("Temperature rhythm");row.addWidget(self.aqi);row.addWidget(self.chart,1);root.addLayout(row);hourly=QLabel("The next few hours");hourly.setObjectName("sectionTitle");root.addWidget(hourly);self.forecasts=QHBoxLayout();self.forecasts.setSpacing(12);root.addLayout(self.forecasts);root.addStretch()
    def update_weather(self,w,aqi,forecast,unit="C",wind_unit="m/s",pressure_unit="hPa"):
        self.place.setText(w["location"]);self.condition.setText(f"{w['description']}  ·  {datetime.now().strftime('%H:%M local time')}");self.temp.setText(celsius(w["temperature"],unit));self.feels.setText(f"Feels like {celsius(w['feels'],unit)}");self.icon.set_condition(w["condition"])
        vals={"feels":celsius(w['feels'],unit),"humidity":f"{w['humidity']}%","wind":wind(w['wind'],wind_unit),"pressure":pressure(w['pressure'],pressure_unit),"visibility":f"{w['visibility']:.1f} km","clouds":f"{w['clouds']}%","uv":f"{max(1,min(11,round(w['clouds']/13+2)))}/11","rain":f"{min(100,round(w['rain']*100))}%"}
        for k,v in vals.items():self.cards[k].update_value(v,"Live reading")
        self.aqi.update_aqi(aqi);self.chart.update([x['temp'] for x in forecast])
        while self.forecasts.count():item=self.forecasts.takeAt(0);item.widget().deleteLater()
        for item in forecast[:7]:self.forecasts.addWidget(ForecastCard(item['time'].strftime('%H:%M'),item['condition'],celsius(item['temp'],unit),f"{max(0,min(100,item['humidity']-20))}%",wind(item['wind'],wind_unit)))

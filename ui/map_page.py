from __future__ import annotations
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QFrame
from PySide6.QtWebEngineWidgets import QWebEngineView
class MapPage(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent);l=QVBoxLayout(self);l.setContentsMargins(26,8,26,28);title=QLabel("Weather map");title.setObjectName("pageTitle");l.addWidget(title);sub=QLabel("Explore live location context with interactive OpenStreetMap controls.");sub.setObjectName("muted");l.addWidget(sub);self.shell=QFrame();self.shell.setObjectName("mapShell");self.box=QVBoxLayout(self.shell);self.box.setContentsMargins(0,0,0,0);self.preview=QLabel("Open this page to load the interactive map.");self.preview.setAlignment(__import__('PySide6').QtCore.Qt.AlignCenter);self.box.addWidget(self.preview);l.addWidget(self.shell,1);self.web=None;self.location={"location":"Chennai","lat":13.0827,"lon":80.2707}
    def showEvent(self,event):
        super().showEvent(event)
        if self.web is None:
            self.preview.deleteLater();self.web=QWebEngineView();self.box.addWidget(self.web);self.update_location(self.location)
    def update_location(self,w):
        self.location=w
        if self.web is None:return
        html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><style>html,body,#map{{height:100%;margin:0;background:#eaf4ff}}.leaflet-control-zoom a{{border-radius:10px!important;margin:5px;color:#5b4bb7}}.leaflet-popup-content-wrapper{{border-radius:16px;font-family:Inter,Arial}}</style></head><body><div id="map"></div><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>const lat={w['lat']},lon={w['lon']};const map=L.map('map',{{zoomControl:true}}).setView([lat,lon],9);L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap contributors'}}).addTo(map);const icon=L.divIcon({{className:'',html:'<div style="font-size:34px;filter:drop-shadow(0 5px 8px #6b5bb888)">☀️</div>',iconSize:[40,40]}});L.marker([lat,lon],{{icon}}).addTo(map).bindPopup('<b>{w['location']}</b><br>SkyPulse weather point').openPopup();</script></body></html>'''
        self.web.setHtml(html,QUrl("https://skypulse.local/"))

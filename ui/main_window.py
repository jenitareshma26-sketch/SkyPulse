from __future__ import annotations
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QStackedWidget,QMessageBox,QCompleter,QScrollArea
from PySide6.QtCore import Qt,QThread,Signal
from components.sidebar import Sidebar
from components.navbar import Navbar
from components.search_bar import SearchBar
from ui.dashboard import Dashboard
from ui.forecast_page import ForecastPage
from ui.map_page import MapPage
from ui.alerts_page import AlertsPage
from ui.settings_page import SettingsPage
from api.weather import WeatherService
from api.air_quality import AirQualityService
from api.geocoder import Geocoder
from api.alerts import AlertService
from database.database import Database
from database.history import HistoryRepository
from utils.animations import fade_in
from components.ambient_background import AmbientBackground
class LookupWorker(QThread):
    done=Signal(dict,object,object); failed=Signal(str)
    def __init__(self,name,lat,lon):super().__init__();self.name,self.lat,self.lon=name,lat,lon
    def run(self):
        try:
            weather=WeatherService().current(self.lat,self.lon,self.name); forecast=WeatherService().forecast(weather); self.done.emit(weather,AirQualityService().current(self.lat,self.lon),forecast)
        except Exception as exc:self.failed.emit(str(exc))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();self.setWindowTitle("SkyPulse Pro");self.resize(1380,870);self.db=Database();self.history=HistoryRepository(self.db);self.current=None;self.worker=None
        root=AmbientBackground();self.setCentralWidget(root);layout=QHBoxLayout(root);layout.setContentsMargins(0,0,16,0);layout.setSpacing(18);self.sidebar=Sidebar();layout.addWidget(self.sidebar);content=QVBoxLayout();content.setContentsMargins(0,17,0,16);content.setSpacing(12);layout.addLayout(content,1);self.nav=Navbar();content.addWidget(self.nav);self.search=SearchBar();content.addWidget(self.search);self.stack=QStackedWidget();content.addWidget(self.stack,1);self.dashboard=Dashboard();self.forecast=ForecastPage();self.map=MapPage();self.alerts=AlertsPage();self.settings=SettingsPage();self.pages={"dashboard":self.dashboard,"forecast":self.forecast,"map":self.map,"alerts":self.alerts,"settings":self.settings}
        self.page_containers={}
        for key,p in self.pages.items():
            scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setFrameShape(QScrollArea.NoFrame);scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);scroll.setWidget(p);self.stack.addWidget(scroll);self.page_containers[key]=scroll
        self.sidebar.page_requested.connect(self.show_page);self.search.submitted.connect(self.search_location);self.nav.location_requested.connect(lambda:self.load_location("Chennai",13.0827,80.2707));self.nav.settings_requested.connect(lambda:self.show_page("settings"));self.nav.unit.clicked.connect(self.toggle_unit);self.settings.changed.connect(self.apply_settings);self.apply_settings();self.load_location("Chennai",13.0827,80.2707)
    def show_page(self,key):self.stack.setCurrentWidget(self.page_containers[key]);fade_in(self.pages[key])
    def search_location(self,text):
        if not text:return
        try:
            if ',' in text and len(text.split(','))==2:
                lat,lon=map(float,text.split(','));self.load_location(text,lat,lon);return
        except ValueError:pass
        results=Geocoder().search(text)
        if results:self.load_location(results[0]['full'],results[0]['lat'],results[0]['lon'])
        else: QMessageBox.information(self,"Location not found","No location could be resolved. Check your connection or search by latitude, longitude.")
    def load_location(self,name,lat,lon):
        if self.worker and self.worker.isRunning():return
        self.search.setText(name);self.worker=LookupWorker(name,lat,lon);self.worker.done.connect(self.receive_weather);self.worker.failed.connect(lambda e:QMessageBox.warning(self,"Weather update failed",e));self.worker.start()
    def receive_weather(self,w,aqi,forecast):
        self.current=(w,aqi,forecast);self.history.add(w['location'],w['lat'],w['lon']);self.render()
    def render(self):
        if not self.current:return
        w,aqi,f=self.current;unit="F" if self.settings.temp.currentIndex() else "C";wind="mph" if self.settings.wind.currentIndex() else "m/s";pressure="mmHg" if self.settings.pressure.currentIndex() else "hPa";self.dashboard.update_weather(w,aqi,f,unit,wind,pressure);self.forecast.update_forecast(f,unit);self.map.update_location(w);self.alerts.update_alerts(AlertService().alerts(w));self.nav.unit.setText("°"+unit)
    def toggle_unit(self):self.settings.temp.setCurrentIndex(1-self.settings.temp.currentIndex());self.render()
    def apply_settings(self):
        from config import ROOT
        try:self.setStyleSheet((ROOT/"themes"/"light.qss").read_text())
        except OSError:pass
        self.render()

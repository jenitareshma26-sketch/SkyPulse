from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QFont,QPainter,QPen
from PySide6.QtWidgets import QFrame,QGridLayout,QHBoxLayout,QLabel,QVBoxLayout,QWidget
from utils.constants import AQI_LABELS
class AQIGauge(QWidget):
    def __init__(self,parent=None):super().__init__(parent);self.value=1;self.setMinimumSize(145,145)
    def set_value(self,value):self.value=value;self.update()
    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);r=self.rect().adjusted(16,16,-16,-16);color=QColor(AQI_LABELS[self.value][1]);p.setPen(QPen(QColor("#dbe7f7"),13,Qt.SolidLine,Qt.RoundCap));p.drawArc(r,145*16,250*16);p.setPen(QPen(color,13,Qt.SolidLine,Qt.RoundCap));p.drawArc(r,145*16,int(250*self.value/5)*16);p.setPen(QColor("#34455f"));p.setFont(QFont("Inter",26,QFont.Weight.Bold));p.drawText(r,Qt.AlignCenter,str(self.value));p.setFont(QFont("Inter",9));p.drawText(r.adjusted(0,38,0,0),Qt.AlignHCenter,"AQI")
class AirQualityCard(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent);self.setObjectName("glassCard");l=QVBoxLayout(self);title=QLabel("Air quality");title.setObjectName("sectionTitle");l.addWidget(title);body=QHBoxLayout();self.gauge=AQIGauge();body.addWidget(self.gauge);right=QVBoxLayout();self.score=QLabel();self.score.setObjectName("aqi");self.advice=QLabel();self.advice.setWordWrap(True);self.advice.setObjectName("muted");right.addWidget(self.score);right.addWidget(self.advice);right.addStretch();body.addLayout(right,1);l.addLayout(body);self.pollutants=QLabel();self.pollutants.setObjectName("pollutants");l.addWidget(self.pollutants);self.update_aqi({"aqi":1,"pm25":0,"pm10":0,"co":0,"so2":0,"no2":0,"o3":0})
    def update_aqi(self,data):
        label,color=AQI_LABELS[data['aqi']];self.gauge.set_value(data['aqi']);self.score.setText(label);self.score.setStyleSheet(f"color:{color}");self.advice.setText("Perfect for a walk, run, or any outdoor plans." if data['aqi']<3 else "Sensitive groups should take breaks during prolonged outdoor activity.");self.pollutants.setText(f"PM2.5  {data['pm25']}   ·   PM10  {data['pm10']}   ·   CO  {data['co']}\nSO₂  {data['so2']}   ·   NO₂  {data['no2']}   ·   O₃  {data['o3']}")

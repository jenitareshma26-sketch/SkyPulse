"""High-DPI vector weather illustration with subtle live motion."""
from __future__ import annotations
from math import cos, pi, sin
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen, QBrush
from PySide6.QtWidgets import QWidget

class WeatherIcon(QWidget):
    def __init__(self, condition: str = "Clear", size: int = 120, parent=None):
        super().__init__(parent); self.condition = condition; self.phase = 0; self.setFixedSize(size, size)
        self.timer = QTimer(self); self.timer.timeout.connect(self._animate); self.timer.start(45)
    def set_condition(self, condition: str) -> None: self.condition = condition; self.update()
    def _animate(self) -> None: self.phase = (self.phase + 1) % 360; self.update()
    def paintEvent(self, event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);r=self.rect();cx,cy=r.center().x(),r.center().y();s=min(r.width(),r.height())/120
        cond=self.condition.lower(); cloud=cond in {"clouds","mist","fog","haze"}; rain=cond in {"rain","drizzle"}; snow="snow" in cond; storm="thunder" in cond
        if "clear" in cond or not (cloud or rain or snow or storm):
            p.setPen(QPen(QColor("#fde68a"),4*s,Qt.SolidLine,Qt.RoundCap));
            for i in range(12):
                a=i*pi/6+self.phase*pi/180; p.drawLine(cx+cos(a)*31*s,cy+sin(a)*31*s,cx+cos(a)*45*s,cy+sin(a)*45*s)
            glow=QLinearGradient(cx-25*s,cy-25*s,cx+30*s,cy+35*s);glow.setColorAt(0,QColor("#fff9c4"));glow.setColorAt(1,QColor("#fbbf24"));p.setBrush(glow);p.setPen(Qt.NoPen);p.drawEllipse(cx-29*s,cy-29*s,58*s,58*s)
        if cloud or rain or snow or storm:
            p.setPen(Qt.NoPen);g=QLinearGradient(cx-45*s,cy-25*s,cx+45*s,cy+35*s);g.setColorAt(0,QColor("#f8fbff"));g.setColorAt(1,QColor("#b8cae8"));p.setBrush(g)
            p.drawEllipse(cx-43*s,cy-2*s,86*s,36*s);p.drawEllipse(cx-25*s,cy-27*s,48*s,48*s);p.drawEllipse(cx+5*s,cy-17*s,50*s,40*s)
        if rain:
            p.setPen(QPen(QColor("#67e8f9"),4*s,Qt.SolidLine,Qt.RoundCap));
            for x in (-28,0,28): p.drawLine(cx+x*s,cy+29*s,cx+(x-7)*s,cy+48*s)
        if snow:
            p.setPen(QPen(QColor("#e0f2fe"),3*s,Qt.SolidLine,Qt.RoundCap));
            for x in (-25,0,25):
                yy=cy+35*s+sin((self.phase+x)*pi/80)*4*s;p.drawLine(cx+x*s-6*s,yy,cx+x*s+6*s,yy);p.drawLine(cx+x*s,yy-6*s,cx+x*s,yy+6*s)
        if storm:
            p.setBrush(QColor("#fde68a"));p.setPen(Qt.NoPen);p.drawPolygon([(cx-2*s,cy+10*s),(cx+18*s,cy+10*s),(cx+2*s,cy+42*s),(cx+7*s,cy+20*s),(cx-12*s,cy+20*s)])
        if cond in {"mist","fog","haze"}:
            p.setPen(QPen(QColor("#dbeafe"),4*s,Qt.SolidLine,Qt.RoundCap));[p.drawLine(cx-42*s,cy+y*s,cx+42*s,cy+y*s) for y in (22,35,48)]

"""A low-key animated pastel background painted behind all workspace content."""
from __future__ import annotations
from math import sin
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPainter, QRadialGradient
from PySide6.QtWidgets import QWidget
class AmbientBackground(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent);self.phase=0;self.timer=QTimer(self);self.timer.timeout.connect(self.advance);self.timer.start(70)
    def advance(self):self.phase+=.025;self.update()
    def paintEvent(self,event):
        p=QPainter(self);p.fillRect(self.rect(),QColor("#eef6ff"));w,h=self.width(),self.height()
        for x,y,color,rad in [(w*.18+sin(self.phase)*40,h*.12,"#c4b5fd",430),(w*.80,h*.18+sin(self.phase*.7)*45,"#a5f3fc",400),(w*.57,h*.83,"#fecdd3",350)]:
            g=QRadialGradient(x,y,rad);g.setColorAt(0,QColor(color));g.setColorAt(1,QColor(color+"00"));p.setBrush(g);p.setPen(Qt.NoPen);p.drawEllipse(int(x-rad),int(y-rad),rad*2,rad*2)

from __future__ import annotations
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor,QFont,QLinearGradient,QPainter,QPixmap
from PySide6.QtWidgets import QSplashScreen
class SplashScreen(QSplashScreen):
    """A short, polished startup sequence that requires no external assets."""
    def __init__(self):
        super().__init__(QPixmap(620,360));self.frame=0;self.timer=QTimer(self);self.timer.timeout.connect(self.render);self.timer.start(45);self.render()
    def render(self):
        self.frame+=1;pix=QPixmap(620,360);p=QPainter(pix);g=QLinearGradient(0,0,620,360);g.setColorAt(0,QColor("#7f7fd5"));g.setColorAt(.52,QColor("#86a8e7"));g.setColorAt(1,QColor("#91eae4"));p.fillRect(pix.rect(),g);pulse=42+(self.frame%30);p.setBrush(QColor(255,255,255,45));p.setPen(Qt.NoPen);p.drawEllipse(310-pulse,118-pulse,pulse*2,pulse*2);p.setPen(QColor("white"));p.setFont(QFont("Inter",52,QFont.Weight.Bold));p.drawText(0,78,620,100,Qt.AlignCenter,"☁");p.setFont(QFont("Inter",25,QFont.Weight.Bold));p.drawText(0,190,620,38,Qt.AlignCenter,"SkyPulse Pro");p.setFont(QFont("Inter",11));p.drawText(0,232,620,25,Qt.AlignCenter,"A more beautiful way to read the sky");p.setBrush(QColor(255,255,255,130));p.drawRoundedRect(205,286,210,5,3,3);p.setBrush(QColor("white"));p.drawRoundedRect(205,286,min(210,(self.frame%55)*4),5,3,3);p.end();self.setPixmap(pix)

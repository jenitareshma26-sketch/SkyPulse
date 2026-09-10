from __future__ import annotations
from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QPainter,QPainterPath,QLinearGradient,QPen
class Sparkline(QLabel):
    def __init__(self):super().__init__();self.values=[];self.setMinimumHeight(124)
    def set_values(self,values):self.values=list(values);self.update()
    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);r=self.rect().adjusted(6,10,-6,-16)
        if len(self.values)<2:return
        low,high=min(self.values),max(self.values);span=max(high-low,.1);path=QPainterPath()
        for i,v in enumerate(self.values):
            x=r.left()+r.width()*i/(len(self.values)-1);y=r.bottom()-(v-low)/span*r.height();path.moveTo(x,y) if i==0 else path.lineTo(x,y)
        fill=QPainterPath(path);fill.lineTo(r.right(),r.bottom());fill.lineTo(r.left(),r.bottom());fill.closeSubpath();g=QLinearGradient(0,r.top(),0,r.bottom());top=QColor("#8b5cf6");top.setAlpha(110);bottom=QColor("#8b5cf6");bottom.setAlpha(0);g.setColorAt(0,top);g.setColorAt(1,bottom);p.fillPath(fill,g);p.setPen(QPen(QColor("#7c3aed"),3));p.drawPath(path)
class ChartCard(QFrame):
    def __init__(self,title,parent=None):
        super().__init__(parent);self.setObjectName("glassCard");self.layout=QVBoxLayout(self);label=QLabel(title);label.setObjectName("sectionTitle");self.layout.addWidget(label);self.plot=Sparkline();self.layout.addWidget(self.plot)
    def update(self,values):self.plot.set_values(values[:24])

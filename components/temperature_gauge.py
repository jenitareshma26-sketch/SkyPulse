from PySide6.QtWidgets import QProgressBar
class TemperatureGauge(QProgressBar):
    def __init__(self,parent=None): super().__init__(parent);self.setRange(-20,50);self.setFormat("%v°")

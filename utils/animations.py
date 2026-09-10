from __future__ import annotations
from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
def fade_in(widget: QWidget, duration: int = 280) -> None:
    effect = QGraphicsOpacityEffect(widget); widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity", widget); animation.setDuration(duration); animation.setStartValue(0.0); animation.setEndValue(1.0); animation.setEasingCurve(QEasingCurve.OutCubic); animation.start(); widget._fade_animation = animation


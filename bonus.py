from PyQt5.QtCore import (
    Qt,
    QRect,
    QBasicTimer,
    QPoint
)
from PyQt5.QtGui import (
    QBrush,
    QPixmap
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)
from PyQt5.QtMultimedia import (
    QSound
)
from game_object import GameObject
import random


BONUSES = ['BONUS_DESTROY', 'BONUS_TANK', 'BONUS_TIME']


class Bonus(GameObject):
    def __init__(self):
        GameObject.__init__(self, random.choice(BONUSES), QPoint(
            random.randint(0, 384), random.randint(0, 384)), 32, 30, 3, False)

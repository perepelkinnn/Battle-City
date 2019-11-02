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

from moveable_object import MoveableObject
from bullet import Bullet
from bullet import BULLET_WIDTH
from bullet import BULLET_HEIGHT


class Tank(MoveableObject):
    def __init__(self, type, position, width, height, drawing_priority,
                 speed, health, max_bullets, strength):
        MoveableObject.__init__(self, type, position,
                                width, height, drawing_priority, speed)
        self.bullets = []
        self.max_count_bullets = max_bullets
        self.health = health
        self.strength = strength
        self.timer_shot = 30

    def make_shot(self, scene):
        bullet = Bullet(self)
        scene.addItem(bullet)
        self.bullets.append(bullet)
        self.timer_shot = 0

    def can_shot(self):
        return self.max_count_bullets > len(self.bullets) and \
            self.timer_shot > 30

    def update(self, scene):
        MoveableObject.update(self, scene)
        self.timer_shot += 1

from PyQt5.QtCore import (
    Qt,
    QRect,
    QRectF,
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
from game_object import GameObject

TYPE = {
    'SMALL': ['EXPLOSION',   QPoint(-11, -10)],
    'MEDIUM': ['EXPLOSION_2', QPoint(-4, -3)],
    'BIG': ['EXPLOSION_3', QPoint(-17, -16)],
}

MAX_TICKS = 20


class Explosion(GameObject):
    def __init__(self, pos, max):
        GameObject.__init__(
            self, TYPE['SMALL'][0], pos + TYPE['SMALL'][1], 0, 0, 1, False)
        self.ticks = 0
        self.max = max

    def update(self, scene):
        self.ticks += 1

        if self.ticks == MAX_TICKS // 3:
            if self.max == 'SMALL':
                self.stop(scene)
            self.next('MEDIUM')

        if self.ticks == MAX_TICKS * 2 // 3:
            if self.max == 'MEDIUM':
                self.stop(scene)
            self.next('BIG')

        if self.ticks == MAX_TICKS or self.type == self.max:
            self.stop(scene)

    def next(self, type):
        self.change_pixmap(TYPE[type][0])
        self.setPos(self.pos() + TYPE[type][1])

    def stop(self, scene):
        scene.removeItem(self)
        scene.map.objects.remove(self)

from PyQt5.QtCore import (
    Qt,
    QRect,
    QBasicTimer,
    QRectF,
    QPoint
)
from PyQt5.QtGui import (
    QPixmap
)
from PyQt5.QtWidgets import (
    QGraphicsPixmapItem
)
from game_object import GameObject


class Flag(GameObject):

    def __init__(self):
        GameObject.__init__(self, 'FLAG_ON', QPoint(192, 384), 32, 32, 1, True)

    def update(self, scene):
        if self.isBroken:
            self.change_pixmap('FLAG_OFF')
            scene.is_game_over = True

    def change_pixmap(self, type):
        self.setPixmap(QPixmap('Sprites/' + type + '.png'))

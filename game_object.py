from PyQt5.QtCore import (
    Qt,
    QRect,
    QBasicTimer,
    QRectF,
    QPoint
)
from PyQt5.QtGui import (
    QPixmap,
    QColor
)
from PyQt5.QtWidgets import (
    QGraphicsPixmapItem
)


class GameObject(QGraphicsPixmapItem):

    def __init__(self, type, pos, width, height, drawing_priority, solid=True):
        QGraphicsPixmapItem.__init__(self)

        self.setTransformOriginPoint(QPoint(width / 2, height / 2))
        self.setPixmap(QPixmap('Sprites/' + type + '.png'))
        self.setZValue(drawing_priority)
        self.setPos(pos)

        self.rect = QRectF(pos.x(), pos.y(), width, height)
        self.type = type
        self.solid = solid
        self.isBroken = False

    def update(self, scene):
        if self.isBroken:
            scene.removeItem(self)
            scene.map.objects.remove(self)

    def change_pixmap(self, type):
        self.setPixmap(QPixmap('Sprites/' + type + '.png'))

    def set_pixmap_red(self):
        img = self.pixmap().toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x, y)
                color.setRed(min(color.red() * 2, 255))
                img.setPixel(x, y, color.rgb())
        self.setPixmap(QPixmap.fromImage(img))

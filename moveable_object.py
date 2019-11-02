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
from bonus import Bonus

TURNS = {
    'UP': 0,
    'DOWN': 180,
    'RIGHT': 90,
    'LEFT': 270
}
VECTORS = {
    'UP': QPoint(0, -1),
    'DOWN': QPoint(0, 1),
    'RIGHT': QPoint(1, 0),
    'LEFT': QPoint(-1, 0),
}


class MoveableObject(GameObject):
    def __init__(self, type, pos, width, height, priority, speed):
        GameObject.__init__(self, type, pos, width, height, priority)
        self.rect = self.create_rect(pos, width, height)
        self.speed = speed
        self.direction = 'UP'
        self.movement_status = 'NORMAL'
        self.last_move = QPoint(0, 0)

    def move(self, direction):
        if self.movement_status == 'STOP':
            return
        self.setRotation(TURNS[direction])
        self.last_move = self.speed * VECTORS[direction]
        self.setPos(self.pos() + self.last_move)
        self.correct_position(direction)
        self.rect.moveTo(self.pos())
        self.direction = direction

    def correct_position(self, new_direction):
        if new_direction == 'UP' or new_direction == 'DOWN':
            dx = self.pos().x() % 16
            delta = QPoint(-dx + 16, 0) if dx // 8 >= 1 else QPoint(-dx, 0)
        else:
            dy = self.pos().y() % 16
            delta = QPoint(0, -dy + 16) if dy // 8 >= 1 else QPoint(0, -dy)
        self.setPos(self.pos() + delta)

    def create_rect(self, pos, width, height):
        if width >= height:
            self.height = width
            return QRectF(pos.x(), pos.y(), width, width)
        self.width = height
        return QRectF(pos.x(), pos.y(), height, height)

    def get_angle(self):
        return TURNS[self.direction]

    def processing_overlap(self, scene, obj):
        if self.type == 'PLAYER' and type(obj) is Bonus:
            scene.map.objects.remove(obj)
            scene.removeItem(obj)
            self.bonus = obj.type
            scene.play_sound('bonus')
        if obj.type == 'ICE':
            self.movement_status = 'GLIDE'
        if not obj.solid:
            return
        if self.type == 'TANK' and obj.type in ['BRICK', 'STEEL'] and \
                self.isBreak:
            scene.map.objects.remove(obj)
            scene.removeItem(obj)
            scene.play_sound('brick')
            return
        if self.type == 'TANK' and obj.type in ['BORDER', 'STEEL']:
            self.timer_move = 150
        self.setPos(self.pos() - self.last_move)
        self.rect.moveTo(self.pos())
        self.last_move = - self.last_move

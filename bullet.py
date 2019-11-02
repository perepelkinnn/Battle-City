from PyQt5.QtCore import (
    Qt,
    QRect,
    QPoint
)

from PyQt5.QtWidgets import (
    QGraphicsScene
)

from moveable_object import MoveableObject
from explosion import Explosion

BULLET_WIDTH = 32
BULLET_HEIGHT = 32
PRIORITY = 1

TANKS = ['PLAYER', 'TANK']


class Bullet(MoveableObject):
    def __init__(self, owner):
        MoveableObject.__init__(self, 'BULLET', owner.pos(), BULLET_WIDTH,
                                BULLET_HEIGHT, PRIORITY, owner.shot_speed)
        self.direction = owner.direction
        self.solid = False
        self.owner = owner
        self.strength = owner.strength

    def update(self, scene):
        self.move(self.direction)
        if self.isBroken:
            self.owner.bullets.remove(self)
            scene.removeItem(self)
            explosion = Explosion(self.rect.center(), 'MEDIUM')
            scene.addItem(explosion)
            scene.map.objects.append(explosion)

    def processing_overlap(self, scene, obj):
        if self.owner == obj or obj.type in ['LEAVES', 'WATER',  'ICE']:
            return
        if obj.type == 'STEEL' and self.strength >= 3 or obj.type == 'BRICK':
            obj.isBroken = True
        if obj.type == 'FLAG_ON':
            obj.isBroken = True
        if (self.owner.type in TANKS and obj.type in TANKS) and \
                not self.isBroken and self.owner.type != obj.type:
            obj.health -= self.strength
            if obj.type == 'TANK' and obj.type_tank == 'ARMOR_TANK':
                obj.change_pixmap(obj.type_tank + str(obj.health))
        if self.owner.type == 'PLAYER':
            if obj.type == 'STEEL' or obj.type == 'TANK' and \
                    obj.type_tank == 'ARMOR_TANK':
                scene.play_sound('steel')
            if obj.type == 'BRICK':
                scene.play_sound('brick')
        self.isBroken = True

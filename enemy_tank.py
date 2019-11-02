from PyQt5.QtCore import (
    Qt,
    QRect,
    QBasicTimer,
    QPoint
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)
import random
import math
from tank import Tank
from explosion import Explosion
from bonus import Bonus

TANKS = {
    '0': {'SPEED': 1, 'SHOT_SPEED': 3, 'MAX': 1,
          'HP': 1, 'IMG': 'TANK', 'VALUE': 100},
    '1': {'SPEED': 3, 'SHOT_SPEED': 5, 'MAX': 1,
          'HP': 1, 'IMG': 'FAST_TANK', 'VALUE': 200},
    '2': {'SPEED': 2, 'SHOT_SPEED': 8, 'MAX': 2,
          'HP': 1, 'IMG': 'POWER_TANK', 'VALUE': 300},
    '3': {'SPEED': 1, 'SHOT_SPEED': 5, 'MAX': 1,
          'HP': 4, 'IMG': 'ARMOR_TANK', 'VALUE': 400},
    '4': {'SPEED': 1, 'SHOT_SPEED': 3, 'MAX': 1,
          'HP': 8, 'IMG': 'FAT_TANK', 'VALUE': 400},
    '5': {'SPEED': 1, 'SHOT_SPEED': 3, 'MAX': 1,
          'HP': 1, 'IMG': 'BREAK_TANK', 'VALUE': 400}
}

WEIGHT = 32
HEIGHT = 32


class EnemyTank(Tank):
    def __init__(self, level, isBonus=False):
        level = str(level)
        Tank.__init__(self, 'TANK', QPoint(0, 0), WEIGHT, HEIGHT, 1,
                      TANKS[level]['SPEED'], TANKS[level]['HP'],
                      TANKS[level]['MAX'], 1)
        self.isBonus = isBonus
        self.timer_move = 60
        self.shot_speed = TANKS[level]['SHOT_SPEED']
        self.change_pixmap(TANKS[level]['IMG'])
        self.type_tank = TANKS[level]['IMG']
        if self.type_tank == 'ARMOR_TANK':
            self.change_pixmap(self.type_tank + str(self.health))
        if isBonus:
            self.set_pixmap_red()
        self.value = TANKS[level]['VALUE']
        self.movement_status = 'STOP'
        self.isBreak = False
        self.chance_shoot = 0.95
        if level == '5':
            self.isBreak = True
        if level == '4':
            self.chance_shoot = 0.99

    def update(self, scene):
        if not scene.freeze_enemys:
            self.move(scene)
            self.shoot(scene)
            self.timer_move += 1
        self.check_hp(scene)
        Tank.update(self, scene)

    def move(self, scene):
        pos = scene.player.pos()
        x = (pos.x() - self.pos().x())
        y = (pos.y() - self.pos().y())
        if math.sqrt(x ** 2 + y ** 2) < 128:
            target = scene.player.pos()
        else:
            target = QPoint(192, 384)
        if self.timer_move > 120:
            dir = target - self.pos()
            angle = math.atan2(dir.y(), dir.x())
            if angle > 0:
                if angle < math.pi / 4:
                    directions = ['DOWN', 'UP', 'RIGHT', 'RIGHT']
                elif angle > 3 * math.pi / 4:
                    directions = ['DOWN', 'LEFT', 'UP', 'LEFT']
                else:
                    directions = ['DOWN', 'LEFT', 'DOWN', 'RIGHT']
            else:
                if angle > -math.pi / 4:
                    directions = ['DOWN', 'RIGHT', 'RIGHT', 'UP']
                elif angle < -3 * math.pi / 4:
                    directions = ['DOWN', 'LEFT', 'UP', 'LEFT']
                else:
                    directions = ['UP', 'LEFT', 'UP', 'RIGHT']

            if self.movement_status == 'STOP':
                self.movement_status = 'NORMAL'
            rand = random.choice(directions)
            self.direction = rand
            self.timer_move = 0
        Tank.move(self, self.direction)

    def shoot(self, scene):
        rand = random.random()
        if rand > self.chance_shoot and self.can_shot():
            self.make_shot(scene)

    def check_hp(self, scene):
        if self.health <= 0:
            scene.removeItem(self)
            scene.enemys.remove(self)
            for bullet in self.bullets:
                scene.removeItem(bullet)
            scene.player.score += self.value
            explosion = Explosion(self.rect.center(), 'BIG')
            scene.addItem(explosion)
            scene.play_sound('explosion')
            scene.map.objects.append(explosion)
            if self.isBonus:
                bonus = Bonus()
                scene.map.objects.append(bonus)
                scene.addItem(bonus)

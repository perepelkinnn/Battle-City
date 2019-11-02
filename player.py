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

from tank import Tank
from explosion import Explosion

TYPE = 'PLAYER'
POSITION = QPoint(144, 384)
WIDTH = 32
HEIGTH = 32
PRIORITY = 1
SPEED = 2
HEALTH = 1
MAX_BULLETS = 1
STRENGHT = 1
LIVES = 3


class Player(Tank):
    def __init__(self):
        Tank.__init__(self, TYPE, POSITION, WIDTH, HEIGTH,
                      PRIORITY, SPEED, HEALTH, MAX_BULLETS, STRENGHT)
        self.score = 0
        self.shot_speed = 5
        self.lives = LIVES
        self.bonus = None
        self.level = 0
        self.freeze_timer = 0

    def processing_keys(self, pressed_keys, scene):
        if len(pressed_keys) > 0:
            if Qt.Key_Space in pressed_keys and scene.player.can_shot():
                scene.player.make_shot(scene)
                scene.play_sound('fire')
            key = pressed_keys[-1]
            if key == Qt.Key_A:
                self.move('LEFT')
            elif key == Qt.Key_W:
                self.move('UP')
            elif key == Qt.Key_D:
                self.move('RIGHT')
            elif key == Qt.Key_S:
                self.move('DOWN')
            return

        if self.movement_status == 'GLIDE':
            self.movement_status = 'NORMAL'
            self.move(self.direction)

    def update(self, scene):
        if self.bonus == 'BONUS_DESTROY':
            self.destroy_enemys(scene)
        elif self.bonus == 'BONUS_TANK':
            self.level_up()
        elif self.bonus == 'BONUS_TIME':
            self.freeze_timer = 0
            scene.freeze_enemys = True
            self.bonus = None
        if scene.freeze_enemys:
            self.freeze_timer += 1
            if self.freeze_timer > 500:
                scene.freeze_enemys = False
        Tank.update(self, scene)
        self.check_hp(scene)
        self.check_lives(scene)

    def level_up(self):
        if self.level == 0:
            self.shot_speed = 8
        elif self.level == 1:
            self.max_count_bullets = 2
        elif self.level == 2:
            self.strength = 3
        elif self.level == 3:
            self.health = 4
        else:
            pass
        self.level += 1
        self.bonus = None

    def check_hp(self, scene):
        if self.health == 0:
            scene.removeItem(self)
            for bullet in self.bullets:
                scene.removeItem(bullet)
            explosion = Explosion(self.rect.center(), 'BIG')
            scene.addItem(explosion)
            scene.play_sound('explosion')
            scene.map.objects.append(explosion)
            self.health = HEALTH
            self.lives -= 1
            scene.init_player(self)

    def check_lives(self, scene):
        if self.lives == 0:
            scene.is_game_over = True

    def destroy_enemys(self, scene):
        for enemy in scene.enemys:
            enemy.health = 0
        self.bonus = None

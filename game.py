from PyQt5.QtCore import (
    Qt,
    QRect,
    QRectF,
    QBasicTimer,
    QPoint,
    QUrl,
    QFile,
    QIODevice
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QPen,
    QFont,
    QFontDatabase,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView
)
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent,
    QSound,
    QAudioFormat,
    QAudioOutput,
    QSoundEffect,
    QMediaPlaylist
)
import sys
import unittest
import time
import random
from threading import Timer
from enemy_tank import EnemyTank
from player import Player
from map import Map
from game_object import GameObject


WIDTH = 416
HEIGHT = 416
OFSET = [30, 20]
SCREEN_WIDTH = 416 + OFSET[0] * 2 + 100
SCREEN_HEIGHT = 416 + OFSET[1] * 2

FPS = 60
POINT_SPAWN = [QPoint(0, 0), QPoint(192, 0), QPoint(384, 0)]
SPAWN_BOXES = [QRectF(0, 0, 32, 32), QRectF(
    192, 0, 32, 32), QRectF(384, 0, 32, 32)]
POINT_PLAYER = QPoint(144, 384)
SPAWN_INTERVAL = 150
COUNT_LEVEL = 3
FIRST_PLAYER_CONTROLS = frozenset([
    Qt.Key_A,
    Qt.Key_S,
    Qt.Key_D,
    Qt.Key_W,
    Qt.Key_Space
])


class Scene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.pressed_keys = []
        self.timer = QBasicTimer()
        self.timer.start(1000 // FPS, self)
        self.timer_spawn = SPAWN_INTERVAL
        self.freeze_enemys = False
        self.new_game()
        self.init_sounds()
        self.play_sound('gamestart')
        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setSceneRect(-OFSET[0], -OFSET[1], SCREEN_WIDTH, SCREEN_HEIGHT)

    def init_sounds(self):
        self.sounds = {
            'fire': QSound('Resourses/Music/fire.wav'),
            'gamestart': QSound('Resourses/Music/gamestart.wav'),
            'steel': QSound('Resourses/Music/steel.wav'),
            'brick': QSound('Resourses/Music/brick.wav'),
            'gameover': QSound('Resourses/Music/gameover.wav'),
            'explosion': QSound('Resourses/Music/explosion.wav'),
            'bonus': QSound('Resourses/Music/bonus.wav'),
        }

    def play_sound(self, name):
        self.sounds[name].play()

    def show_text(self, text, size):
        self.update()
        window_bg = QGraphicsRectItem()
        window_bg.setRect(-OFSET[0], -OFSET[1], SCREEN_WIDTH, SCREEN_HEIGHT)
        window_bg.setBrush(QBrush(Qt.black))
        self.addItem(window_bg)
        self.text = QGraphicsTextItem(text)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setPos(window_bg.rect().center() - QPoint(120, size))
        self.text.setFont(QFont('Press Start', int(size)))
        self.addItem(self.text)

    def init_text(self):
        QFontDatabase.addApplicationFont('game_font.ttf')

        self.text_score = QGraphicsTextItem('SCORE')
        self.text_score.setDefaultTextColor(Qt.black)
        self.text_score.setPos(426, 0)
        self.text_score.setFont(QFont('Press Start', 14))
        self.addItem(self.text_score)

        self.score = QGraphicsTextItem(str(0))
        self.score.setPos(426, 30)
        self.score.setFont(QFont('Press Start', 14))
        self.score.setDefaultTextColor(Qt.black)
        self.addItem(self.score)

        self.text_tanks = QGraphicsTextItem('TANKS')
        self.text_tanks.setDefaultTextColor(Qt.black)
        self.text_tanks.setPos(426, 60)
        self.text_tanks.setFont(QFont('Press Start', 14))
        self.addItem(self.text_tanks)

        self.count_enemys = QGraphicsTextItem(str(len(self.map.all_enemys)))
        self.count_enemys.setPos(426, 90)
        self.count_enemys.setFont(QFont('Press Start', 14))
        self.count_enemys.setDefaultTextColor(Qt.black)
        self.addItem(self.count_enemys)

        self.lives_text = QGraphicsTextItem('LIVES')
        self.lives_text.setDefaultTextColor(Qt.black)
        self.lives_text.setPos(426, 120)
        self.lives_text.setFont(QFont('Press Start', 14))
        self.addItem(self.lives_text)

        self.count_lives = QGraphicsTextItem(str(self.player.lives))
        self.count_lives.setPos(426, 150)
        self.count_lives.setFont(QFont('Press Start', 14))
        self.count_lives.setDefaultTextColor(Qt.black)
        self.addItem(self.count_lives)

    def keyPressEvent(self, event):
        if event.key() in FIRST_PLAYER_CONTROLS:
            if event.key() == Qt.Key_Space:
                self.pressed_keys.insert(0, event.key())
            else:
                self.pressed_keys.append(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in FIRST_PLAYER_CONTROLS:
            self.pressed_keys.remove(event.key())

    def timerEvent(self, event):
        self.update_scene()
        self.update()

    def player_update(self):
        self.player.processing_keys(self.pressed_keys, self)
        self.player.update(self)
        self.score.setPlainText(str(self.player.score))
        self.count_lives.setPlainText(str(self.player.lives))
        self.count_enemys.setPlainText(
            str(len(self.map.all_enemys) + len(self.enemys)))

    def player_collision_enemys(self):
        for enemy in self.enemys:
            if self.player.rect.intersects(enemy.rect):
                self.player.processing_overlap(self, enemy)

    def enemys_update(self):
        for enemy in self.enemys:
            enemy.update(scene)
            self.enemy_collision_enemys(enemy)

    def enemys_collision_player(self):
        for enemy in self.enemys:
            if enemy.rect.intersects(self.player.rect):
                enemy.processing_overlap(self, self.player)

    def enemy_collision_enemys(self, enemy):
        for other in self.enemys:
            if enemy.rect.intersects(other.rect) and other != enemy:
                enemy.processing_overlap(self, other)

    def player_bullets_update(self):
        for bullet in self.player.bullets:
            bullet.update(self)

    def player_bullets_collision_enemys(self):
        for bullet in self.player.bullets:
            for enemy in self.enemys:
                if bullet.rect.intersects(enemy.rect):
                    bullet.processing_overlap(self, enemy)

    def enemys_bullets_update(self):
        for enemy in self.enemys:
            for bullet in enemy.bullets:
                bullet.update(self)

    def enemys_bullets_collision_player_enemys_player_bullets(self):
        for enemy in self.enemys:
            for bullet in enemy.bullets:
                if bullet.rect.intersects(self.player.rect):
                    bullet.processing_overlap(self, self.player)
                for other in self.enemys:
                    if bullet.rect.intersects(other.rect):
                        bullet.processing_overlap(self, other)
                for player_bullet in self.player.bullets:
                    if bullet.rect.intersects(player_bullet.rect):
                        bullet.processing_overlap(self, player_bullet)
                        player_bullet.processing_overlap(self, bullet)

    def moveable_obj_collision_static_obj(self):
        for obj in self.map.objects:
            obj.update(self)
            if self.player.rect.intersects(obj.rect) and \
                    obj.type != self.player:
                self.player.processing_overlap(self, obj)
            for enemy in self.enemys:
                if enemy.rect.intersects(obj.rect) and obj.type != enemy:
                    enemy.processing_overlap(self, obj)
            for bullet in self.player.bullets:
                if bullet.rect.intersects(obj.rect) and obj.type != bullet:
                    bullet.processing_overlap(self, obj)
            for enemy in self.enemys:
                for bullet in enemy.bullets:
                    if bullet.rect.intersects(obj.rect):
                        bullet.processing_overlap(self, obj)

    def spawn_tank(self):
        if self.freeze_enemys:
            return
        for spawn_box in SPAWN_BOXES:
            for enemy in self.enemys:
                if spawn_box.intersects(enemy.rect):
                    return
            if spawn_box.intersects(self.player.rect):
                return
        if len(self.enemys) < 4 and self.timer_spawn > SPAWN_INTERVAL and \
                len(self.map.all_enemys) > 0:
            tank = self.map.all_enemys.pop()
            tank.setPos(random.choice(POINT_SPAWN))
            self.enemys.append(tank)
            self.addItem(tank)
            self.timer_spawn = 0
        self.timer_spawn += 1

    def check_end(self):
        if len(self.enemys) + len(self.map.all_enemys) == 0:
            self.next_level()
        if self.is_game_over:
            self.show_game_over()

    def next_level(self):
        self.remove_all()
        self.init_background()
        self.init_map((self.current_level + 1) % COUNT_LEVEL)
        self.init_player(self.player)
        self.init_text()

    def init_map(self, level=0):
        self.current_level = level
        self.map = Map(level)
        self.enemys = []
        for item in self.map.objects:
            self.addItem(item)

    def init_player(self, player=None):
        if player is None:
            player = Player()
        self.player = player
        self.player.setPos(POINT_PLAYER)
        self.addItem(self.player)

    def init_background(self):
        window_bg = QGraphicsRectItem()
        window_bg.setRect(-OFSET[0], -OFSET[1], SCREEN_WIDTH, SCREEN_HEIGHT)
        window_bg.setBrush(QBrush(QColor(130, 128, 129)))
        self.addItem(window_bg)

        game_bg = QGraphicsRectItem()
        game_bg.setRect(0, 0, WIDTH - 1, HEIGHT - 1)
        game_bg.setBrush(QBrush(Qt.black))
        self.addItem(game_bg)

    def new_game(self):
        self.is_game_over = False
        self.current_level = 0
        self.init_background()
        self.init_map()
        self.init_player()
        self.init_text()

    def show_game_over(self):
        self.remove_all()
        self.show_text('GAME OVER', 20)
        self.play_sound('gameover')

    def remove_all(self):
        for item in self.items():
            self.removeItem(item)

    def update_scene(self):
        if self.is_game_over:
            pass
        else:
            self.player_update()
            self.player_collision_enemys()
            self.enemys_update()
            self.enemys_collision_player()
            self.player_bullets_update()
            self.player_bullets_collision_enemys()
            self.enemys_bullets_update()
            self.enemys_bullets_collision_player_enemys_player_bullets()
            self.moveable_obj_collision_static_obj()
            self.spawn_tank()
            self.check_end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene()
    sys.exit(app.exec_())

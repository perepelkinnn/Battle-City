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
import pytest
import sys
from map import Map
from flag import Flag
from game import Scene
from bullet import Bullet
from player import Player
from enemy_tank import EnemyTank
from explosion import Explosion
from moveable_object import MoveableObject
from bonus import Bonus
from game_object import GameObject


app = QApplication(sys.argv)
map = Map()
flag = Flag()
scene = Scene()
player = Player()
bullet = Bullet(player)


@pytest.fixture
def test_map_init():
    assert type(map) == Map


def test_map_init_level():
    assert len(map.objects) > 0
    assert len(map.all_enemys) > 0


def test_map_init_borders():
    result = False
    for obj in map.objects:
        if obj.type == 'BORDER':
            result = True
    assert result


def test_flag_init():
    assert type(flag) == Flag


def test_flag_update():
    flag.isBroken = True
    flag.update(scene)
    assert scene.is_game_over


def test_bullet_update():
    player.bullets.append(bullet)
    scene.addItem(bullet)
    pos = bullet.pos()
    bullet.isBroken = True
    bullet.update(scene)
    assert pos != bullet.pos()


def test_bullet_overlap():
    bullet = Bullet(player)
    tank = map.all_enemys.pop()
    bullet.processing_overlap(scene, tank)
    assert bullet.isBroken


def test_player_press_key():
    player.processing_keys([Qt.Key_W, Qt.Key_Space], scene)
    assert player.direction == 'UP'


def test_player_update():
    player.bonus = 'BONUS_TIME'
    player.update(scene)
    assert scene.freeze_enemys


def test_player_level_up():
    player.level = 3
    player.level_up()
    assert player.health == 4


def test_player_check_hp():
    player.health = 0
    scene.addItem(player)
    player.check_hp(scene)
    assert player.lives == 2


def test_player_destroy_enemys():
    enemy = EnemyTank('4')
    scene.enemys.append(enemy)
    player.destroy_enemys(scene)
    assert enemy.health == 0


def test_enemy_update():
    scene.freeze_enemys = False
    enemy = map.all_enemys.pop()
    pos = enemy.pos()
    scene.addItem(enemy)
    scene.enemys.append(enemy)
    enemy.health = 0
    enemy.timer_move = 150
    enemy.update(scene)
    assert pos != enemy.pos()


def test_explosion():
    exp = Explosion(QPoint(0, 0), 'BIG')
    scene.addItem(exp)
    scene.map.objects.append(exp)
    exp.ticks = 5
    exp.update(scene)
    pos = exp.pos()
    assert QPoint(0, 0) != pos
    exp.ticks = 12
    exp.update(scene)
    assert pos != exp.pos()


def test_moveable_obj_move():
    player.move('UP')
    assert player.pos().y() == 382
    player.move('DOWN')
    assert player.pos().y() == 384
    player.move('RIGHT')
    assert player.pos().x() == 146
    player.move('LEFT')
    assert player.pos().x() == 144


def test_moveable_obj_correct():
    player.correct_position('RIGHT')
    player.correct_position('UP')
    assert player.pos().y() == 384


def test_moveable_obj_rect():
    rect = player.create_rect(QPoint(0, 0), 10, 20)
    assert rect == QRectF(0, 0, 20, 20)
    rect = player.create_rect(QPoint(0, 0), 20, 10)
    assert rect == QRectF(0, 0, 20, 20)


def test_moveable_obj_angle():
    assert player.get_angle() == 270


def test_moveable_obj_overlap():
    bonus = Bonus()
    scene.addItem(bonus)
    scene.map.objects.append(bonus)
    player.processing_overlap(scene, bonus)
    assert player.bonus is not None


def test_moveable_obj_overlap_break():
    tank = EnemyTank('5')
    brick = GameObject('BRICK', QPoint(0, 0), 32, 32, 1, True)
    scene.addItem(brick)
    scene.map.objects.append(brick)
    length = len(scene.items())
    tank.processing_overlap(scene, brick)
    assert length > len(scene.items())


def test_game():
    scene = Scene()
    scene.update_scene()
    assert True

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

from game_object import GameObject
from enemy_tank import EnemyTank
from flag import Flag

BLOCK_SIZE = 16
WIDTH = 416
HEIGHT = 416
TILES = ['B', 'S', 'L', 'I', 'W']
ENEMYS = ['0', '1', '2', '3', '4', '5']
TILE_TO_TYPE = {
    'B': ('BRICK',  1, True),
    'S': ('STEEL',  1, True),
    'L': ('LEAVES', 2, False),
    'I': ('ICE',    0, False),
    'W': ('WATER',  1, True)
}


class Map:
    def __init__(self, level=0):
        self.objects = []
        self.all_enemys = []
        self.__init_level__(level)
        self.__init_borders__(WIDTH, HEIGHT)
        self.objects.append(Flag())

    def __init_level__(self, level):
        path = 'Levels/level_' + str(level) + '.txt'
        file = open(path, 'r')
        data = file.read().split('\n')
        y = 0
        counter = 0
        for string in data:
            x = 0
            for char in string:

                if char in ENEMYS:
                    counter += 1
                    if counter in [20, 15, 10, 5]:
                        self.all_enemys.append(EnemyTank(char, True))
                    else:
                        self.all_enemys.append(EnemyTank(char))
                if char in TILES:
                    type = TILE_TO_TYPE[char]
                    obj = GameObject(type[0], QPoint(
                        x, y), BLOCK_SIZE, BLOCK_SIZE, type[1], type[2])
                    self.objects.append(obj)

                x += BLOCK_SIZE
            y += BLOCK_SIZE
        file.close()

    def __init_borders__(self, width, height):
        borders = [GameObject('BORDER', QPoint(-1, -1), width, 1, 1),
                   GameObject('BORDER', QPoint(-1, -1), 1, height, 1),
                   GameObject('BORDER', QPoint(0, height), width, 1, 1),
                   GameObject('BORDER', QPoint(width, 0), 1, height, 1)]
        self.objects += borders

from pico2d import load_image

import game_world
from background import Bg


class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        self.x, self.y = 0, 0
        self.width = 50

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

positions = []

def stage1_1():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 (150, 130), (250, 130),
                 (550, 130), (650, 130)
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

def get_ground_positions():
    return positions
from pico2d import load_image, draw_rectangle

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPH = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPH / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 9.8  # 중력 가속도 (m/s²)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_SEC = FRAMES_PER_ACTION * ACTION_PER_TIME

class Monster:
    def __init__(self, x, y):
        self.image = load_image('monster.png')
        self.x, self.y = x, y
        self.frame = 0
        self.direction = 1

        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.gold = 0
        self.exp = 0

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def do(self):
        #self.frame = (self.frame + FRAMES_PER_SEC * game_framework.frame_time) % 4
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        pass

    def set_stat(self, hp, attack, defense, speed, gold, exp):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.gold = gold
        self.exp = exp
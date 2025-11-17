import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world

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
    def __init__(self):
        self.moving = 300
        self.image = load_image('monster.png')
        self.x, self.y = 0, 0
        self.frame = 0
        self.direction = 1
        self.move = 0
        self.size_x1 = 0
        self.size_y1 = 0
        self.size_x2 = 0
        self.size_y2 = 0

        self.max_hp = 0
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.gold = 0
        self.exp = 0

        self.immune_time = 0

    def update(self):
        if self.immune_time > 0.0:
            self.immune_time -= game_framework.frame_time
            if self.immune_time < 0.0:
                self.immune_time = 0.0

        #self.frame = (self.frame + FRAMES_PER_SEC * game_framework.frame_time) % 2
        if self.moving == 0:
            self.move = random.randint(-1, 1)
            self.moving = 300

        if self.move == 1:
            self.direction = 1
            self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time * self.speed / 100
            self.moving -= 1
        elif self.move == -1:
            self.direction = -1
            self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time * self.speed / 100
            self.moving -= 1
        else:
            self.moving -= 1

        if self.x < 20:
            self.x = 20
        elif self.x > 780:
            self.x = 780

    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        draw_rectangle(*self.get_bb())
        draw_rectangle(self.x - self.size_x1, self.y + self.size_y2, self.x - self.size_x1 + 100 * self.hp / self.max_hp, self.y + self.size_y2 + 10, 255, 0, 0, filled=True)
        draw_rectangle(self.x - self.size_x1, self.y + self.size_y2, self.x - self.size_x1 + 100, self.y + self.size_y2 + 10)

    def do(self):
        pass

    def get_bb(self):
        return self.x - self.size_x1, self.y - self.size_y1, self.x + self.size_x2, self.y + self.size_y2

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            #game_world.remove_object(self)
            if self.immune_time == 0:
                self.immune_time = 0.5
                print('monster hit')
                damage = other.damage * (other.attack / 100) * ((100 - self.defense) / 100)
                self.hp -= damage
                print(f'monster hp: {self.hp}/{self.max_hp}')
                if self.hp <= 0:
                    game_world.remove_object(self)
                    other.char.money += self.gold
                    other.char.exp += self.exp

    def set_size(self, size_x1, size_y1, size_x2, size_y2):
        self.size_x1 = size_x1
        self.size_y1 = size_y1
        self.size_x2 = size_x2
        self.size_y2 = size_y2

    def set_stat(self, hp, attack, defense, speed, gold, exp):
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.gold = gold
        self.exp = exp

    def set_image(self, image):
        self.image = load_image(image)
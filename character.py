from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_d, SDLK_a, SDLK_SPACE
from state_machine import StateMachine
from stage import get_ground_positions
import game_world
import game_framework
import math

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 36.0
RUN_SPEED_MPH = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPH / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 9.8  # 중력 가속도 (m/s²)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_SEC = FRAMES_PER_ACTION * ACTION_PER_TIME

class Idle:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        self.char.frame = 0
        if space_down(e):
            if self.char.jumping == 0:
                self.char.jumping = 1
                self.char.yv = abs(self.char.falling_speed * math.sin(math.radians(45.0)))

    def exit(self, event):
        pass

    def do(self):
        pass

    def draw(self):
        if self.char.face_dir == 1:
            self.char.image.clip_draw(self.char.frame * 100, 0, 100, 100, self.char.x, self.char.y)
        else:
            self.char.image.clip_draw(self.char.frame * 100, 200, 100, 100, self.char.x, self.char.y)

class Char:
    def __init__(self):
        self.stage = '1_1'
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.falling_speed = 12
        self.jumping = 0

        self.yv = 0 # m/s
        self.image = load_image('char_image.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.IDLE, left_down: self.MOVE, right_down: self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE: {space_down: self.MOVE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        if self.jumping == 1:
            self.yv -= GRAVITY * game_framework.frame_time

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 30, self.y - 50, self.x + 10, self.y + 10
        else:
            return self.x - 10, self.y - 50, self.x + 30, self.y + 10

    def handle_collision(self, group, other):
        if group == 'char:ground':
            if self.jumping == 1:
                if self.yv < 0:
                    self.jumping = 0
                    self.yv = 0


class Move:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.char.face_dir = 1
        elif left_down(e) or right_up(e):
            self.char.face_dir = -1
        if space_down(e):
            if self.char.jumping == 0:
                self.char.jumping = 1
                self.char.yv = abs(self.char.falling_speed * math.sin(math.radians(45.0)))

    def exit(self, e):
        pass

    def do(self):
        self.char.frame = (self.char.frame + FRAMES_PER_SEC * game_framework.frame_time) % 3
        self.char.x += self.char.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.char.x < 20:
            self.char.x = 20
        elif self.char.x > 780:
            self.char.x = 780

    def draw(self):
        if self.char.face_dir == 1:
            self.char.image.clip_draw(int(self.char.frame) * 100, 0, 100, 100, self.char.x, self.char.y)
        else:
            self.char.image.clip_draw(int(self.char.frame) * 100, 200, 100, 100, self.char.x, self.char.y)


class Attack:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        self.char.frame = 0

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
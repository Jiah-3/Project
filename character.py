from pico2d import load_image, draw_rectangle, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_d, SDLK_a, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
from state_machine import StateMachine
from stage import get_ground_positions
import game_world
import game_framework
import math

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

class Idle:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        self.char.frame = 0
        if space_down(e):
            if self.char.jumping:
                if self.char.yv == 0:
                    #self.char.jumping = False
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
        self.x, self.y = 400, 89
        self.frame = 0
        self.face_dir = 1
        self.falling_speed = 12
        self.jumping = True

        self.yv = 0 # m/s
        self.image = load_image('char_image.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {mouse_L_down: self.ATTACK, space_down: self.IDLE, left_down: self.MOVE, right_down: self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE: {mouse_L_down: self.ATTACK, space_down: self.MOVE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
                self.ATTACK: {time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        if self.jumping:
            self.yv -= GRAVITY * game_framework.frame_time

        if self.y < 89:
            self.y = 89
            self.yv = 0

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
            if self.yv < 0:
                    #self.jumping = True
                    dummy = self.yv
                    self.yv = 0
                    self.y = int(self.y)
                    if self.y % 100 != 89:
                        self.yv = dummy


class Move:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.char.face_dir = 1
        elif left_down(e) or right_up(e):
            self.char.face_dir = -1
        if space_down(e):
            if self.char.jumping:
                if self.char.yv == 0:
                    #self.char.jumping = False
                    self.char.yv = abs(self.char.falling_speed * math.sin(math.radians(45.0)))

    def exit(self, e):
        pass

    def do(self):
        self.char.frame = (self.char.frame + FRAMES_PER_SEC * game_framework.frame_time) % 4
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
        self.char.wait_time = get_time()
        self.char.frame = 0
        game_world.add_object(self, 2)
        game_world.add_collision_pair('attack:monster', self, None)

    def exit(self, e):
        game_world.remove_object(self)

    def do(self):
        self.char.frame = (self.char.frame + FRAMES_PER_SEC * game_framework.frame_time) % 4
        if get_time() - self.char.wait_time > 0.25:
            self.char.state_machine.handle_state_event(('TIME_OUT', None))

    def get_bb(self):
        if self.char.face_dir == 1:
            return self.char.x + 10, self.char.y - 50, self.char.x + 35, self.char.y + 5
        else:
            return self.char.x - 10, self.char.y - 50, self.char.x - 35, self.char.y + 5

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.char.face_dir == 1:
            self.char.image.clip_draw(int(self.char.frame) * 100, 100, 100, 100, self.char.x, self.char.y)
        else:
            self.char.image.clip_draw(int(self.char.frame) * 100, 300, 100, 100, self.char.x, self.char.y)

    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'attack:monster':
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

def mouse_L_down(e):
    if e[0] != 'INPUT' or e[1].type != SDL_MOUSEBUTTONDOWN:
        return False
    b = getattr(e[1], 'button', None)
    # b가 정수일 수도 있고, 객체일 수도 있으므로 안전하게 검사
    if isinstance(b, int):
        return b == SDL_BUTTON_LEFT
    return getattr(b, 'button', None) == SDL_BUTTON_LEFT

def time_out(e):
    return e[0] == 'TIME_OUT'
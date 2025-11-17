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

class Char:
    def __init__(self):
        self.immune_time = 0
        self.x, self.y = 30, 89
        self.frame = 0
        self.face_dir = 1
        self.falling_speed = 12
        self.jumping = True
        self.attacking = False

        self.max_hp = 100
        self.hp = 100
        self.damage = 2
        self.attack = 100
        self.defense = 0
        self.speed = 100
        self.crit_chance = 0

        self.yv = 0 # m/s
        self.image = load_image('char_image.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {mouse_L_down: self.IDLE, space_down: self.IDLE, left_down: self.MOVE, right_down: self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE: {mouse_L_down: self.MOVE, space_down: self.MOVE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
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

        if self.immune_time > 0.0:
            self.immune_time -= game_framework.frame_time
            if self.immune_time < 0.0:
                self.immune_time = 0.0

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.draw_hp_bar()

    def draw_hp_bar(self):
        draw_rectangle(10, 20, 10 + 100 * self.hp / self.max_hp, 21)
        draw_rectangle(10, 22, 10 + 100 * self.hp / self.max_hp, 23)
        draw_rectangle(10, 24, 10 + 100 * self.hp / self.max_hp, 25)
        draw_rectangle(10, 26, 10 + 100 * self.hp / self.max_hp, 27)
        draw_rectangle(10, 28, 10 + 100 * self.hp / self.max_hp, 29)

        draw_rectangle(9, 19, 110, 30)

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

        if group == 'char:monster':
            if self.immune_time == 0:
                self.immune_time = 0.5
                print('player hit')
                damage = other.attack * ((100 - self.defense) / 100)
                self.hp -= damage
                print(f'player hp: {self.hp}/{self.max_hp}')

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
        if mouse_L_down(e) and not self.char.attacking:
            self.char.flame = 0
            self.char.attacking = True
            global attack
            attack = Attack(self.char)
            game_world.add_object(attack, 0)
            game_world.add_collision_pair('attack:monster', attack, None)

    def exit(self, event):
        pass

    def do(self):
        self.char.frame = (self.char.frame + FRAMES_PER_SEC * game_framework.frame_time) % 4
        if self.char.attacking:
            if int(self.char.frame) == 3:
                self.char.attacking = False
                self.char.frame = 0
                game_world.remove_object(attack)

    def draw(self):
        if not self.char.attacking:
            if self.char.face_dir == 1:
                self.char.image.clip_draw(int(self.char.frame) * 100, 0, 100, 100, self.char.x, self.char.y)
            else:
                self.char.image.clip_draw(int(self.char.frame) * 100, 200, 100, 100, self.char.x, self.char.y)
        else:
            if self.char.face_dir == 1:
                self.char.image.clip_draw(int(self.char.frame) * 100, 100, 100, 100, self.char.x, self.char.y)
            else:
                self.char.image.clip_draw(int(self.char.frame) * 100, 300, 100, 100, self.char.x, self.char.y)


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
        if mouse_L_down(e) and not self.char.attacking:
            self.char.flame = 0
            self.char.attacking = True
            global attack
            attack = Attack(self.char)
            game_world.add_object(attack, 1)
            game_world.add_collision_pair('attack:monster', attack, None)

    def exit(self, e):
        pass

    def do(self):
        self.char.frame = (self.char.frame + FRAMES_PER_SEC * game_framework.frame_time) % 4
        self.char.x += self.char.face_dir * RUN_SPEED_PPS * game_framework.frame_time * self.char.speed / 100
        if self.char.x < 20:
            self.char.x = 20
        elif self.char.x > 780:
            self.char.x = 780
        if self.char.attacking:
            if int(self.char.frame) == 3:
                self.char.attacking = False
                self.char.frame = 0
                game_world.remove_object(attack)

    def draw(self):
        if not self.char.attacking:
            if self.char.face_dir == 1:
                self.char.image.clip_draw(int(self.char.frame) * 100, 0, 100, 100, self.char.x, self.char.y)
            else:
                self.char.image.clip_draw(int(self.char.frame) * 100, 200, 100, 100, self.char.x, self.char.y)
        else:
            if self.char.face_dir == 1:
                self.char.image.clip_draw(int(self.char.frame) * 100, 100, 100, 100, self.char.x, self.char.y)
            else:
                self.char.image.clip_draw(int(self.char.frame) * 100, 300, 100, 100, self.char.x, self.char.y)


class Attack:
    def __init__(self, char):
        self.char = char
        self.damage = char.damage
        self.attack = char.attack

    def do(self):
        pass

    def get_bb(self):
        if self.char.face_dir == 1:
            return self.char.x + 10, self.char.y - 40, self.char.x + 35, self.char.y + 5
        else:
            return self.char.x - 35, self.char.y - 40, self.char.x - 10, self.char.y + 5

    def draw(self):
        draw_rectangle(*self.get_bb())

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
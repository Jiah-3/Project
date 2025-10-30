from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_d, SDLK_a
from state_machine import StateMachine

class Idle:
    def __init__(self, char):
        self.char = char

    def enter(self, event):
        self.char.frame = 0

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
        self.image = load_image('char_image.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {left_down: self.MOVE, right_down: self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

class Move:
    def __init__(self, char):
        self.char = char

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.char.face_dir = 1
        elif left_down(e) or right_up(e):
            self.char.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.char.frame = (self.char.frame + 1) % 3
        self.char.x += self.char.face_dir * 5
        if self.char.x < 20:
            self.char.x = 20
        elif self.char.x > 780:
            self.char.x = 780

    def draw(self):
        if self.char.face_dir == 1:
            self.char.image.clip_draw(self.char.frame * 100, 0, 100, 100, self.char.x, self.char.y)
        else:
            self.char.image.clip_draw(self.char.frame * 100, 200, 100, 100, self.char.x, self.char.y)

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


import random

from pico2d import load_image, draw_rectangle, load_font, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_d, SDLK_a, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDLK_e, \
    SDLK_s, SDLK_l

import character_state
import inventory_mode
import drawing_bb
from state_machine import StateMachine
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

grey_bear_skill1 = 0
grey_bear_skill2 = 0

current_time = 0
past_time = 0

class Char:
    def __init__(self):
        self.immune_time = 0
        self.x, self.y = 30, 90
        self.frame = 0
        self.face_dir = 1
        self.falling_speed = 12
        self.poisoned = 0.0
        self.poison_acc = 0.0
        self.jumping = True
        self.attacking = False
        self.level_image = load_image('level.png')
        self.font = load_font('ENCR10B.TTF', 10)
        if character_state.char is None:
            self.stage = '1_1'
            self.stat_points = 0
            self.stat_hp = 0
            self.stat_attack = 1000
            self.stat_defense = 0
            self.stat_agility = 0
            self.stat_luck = 0

            self.gold = 0
            self.exp = 0
            self.prev_level_exp = 1
            self.next_level_exp = 1
            self.level = 0

            self.max_hp = 100 + self.stat_hp * 1
            self.hp = 100 + self.stat_hp * 1
            self.damage = 2 + self.stat_attack * 0.05
            self.attack = 100
            self.defense = 0 + self.stat_defense * 0.5
            self.speed = 100 + self.stat_agility * 1
            self.crit_chance = 0 + self.stat_luck * 1
            self.dodge = 0 + self.stat_agility * 0.1
            self.gold_bonus = 0

            self.item_max_hp = 0
            self.item_damage = 0
            self.item_attack = 0
            self.item_defense = 0
            self.item_speed = 0
            self.item_crit_chance = 0
            self.item_dodge = 0
        else:
            self.char = character_state.char
            self.stage = character_state.char.stage

            self.stat_points = character_state.char.stat_points
            self.stat_hp = character_state.char.stat_hp
            self.stat_attack = character_state.char.stat_attack
            self.stat_defense = character_state.char.stat_defense
            self.stat_agility = character_state.char.stat_agility
            self.stat_luck = character_state.char.stat_luck

            self.gold = character_state.char.gold
            self.exp = character_state.char.exp
            self.prev_level_exp = character_state.char.prev_level_exp
            self.next_level_exp = character_state.char.next_level_exp
            self.level = character_state.char.level

            self.max_hp = character_state.char.max_hp
            self.hp = character_state.char.hp
            self.damage = character_state.char.damage
            self.attack = character_state.char.attack
            self.defense = character_state.char.defense
            self.speed = character_state.char.speed
            self.crit_chance = character_state.char.crit_chance
            self.dodge = character_state.char.dodge
            self.char.gold_bonus = character_state.char.gold_bonus

            self.item_max_hp = 0
            self.item_damage = 0
            self.item_attack = 0
            self.item_defense = 0
            self.item_speed = 0
            self.item_crit_chance = 0
            self.item_dodge = 0

        #아이템 초기화
        self.item = [
            None, None, None,
            None, None, None,
            None, None, None,
        ]

        self.yv = 0 # m/s
        self.image = load_image('char_image.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {l_down: self.IDLE, s_down: self.IDLE, e_down: self.IDLE, mouse_L_down: self.IDLE, space_down: self.IDLE, left_down: self.MOVE, right_down: self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE: {l_down: self.MOVE, s_down: self.MOVE, e_down: self.MOVE, mouse_L_down: self.MOVE, space_down: self.MOVE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        update_items()
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        if self.jumping:
            self.yv -= GRAVITY * game_framework.frame_time

        if self.immune_time > 0.0:
            self.immune_time -= game_framework.frame_time
            if self.immune_time < 0.0:
                self.immune_time = 0.0

        if self.next_level_exp <= self.exp:
            self.level += 1
            self.stat_points += 4
            self.exp -= self.next_level_exp
            self.prev_level_exp, self.next_level_exp = self.next_level_exp, self.prev_level_exp + self.next_level_exp

        if self.y <= -100:
            self.y = 900

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        character_state.char = self

        global grey_bear_skill1
        if grey_bear_skill1 != 0 and get_time() - grey_bear_skill1 >= 0.25:
            grey_bear_skill1 = 0

        global grey_bear_skill2
        if grey_bear_skill2 != 0 and get_time() - grey_bear_skill2 >= 0.25:
            grey_bear_skill2 = 0

        if self.poisoned > 0.0:
            self.poisoned -= game_framework.frame_time
            if self.poisoned < 0.0:
                self.poisoned = 0.0

            self.poison_acc += game_framework.frame_time
            while self.poison_acc >= 0.1:
                self.hp -= 0.5
                self.poison_acc -= 0.1

            if self.poisoned == 0.0:
                self.poison_acc = 0.0

        if self.hp <= 0:
            self.char = character_state.char

            self.gold = 0
            self.max_hp = 100 + self.stat_hp * 1
            self.hp = 100 + self.stat_hp * 1
            self.damage = 2 + self.stat_attack * 0.05
            self.attack = 100
            self.defense = 0 + self.stat_defense * 0.5
            self.speed = 100 + self.stat_agility * 1
            self.crit_chance = 0 + self.stat_luck * 1
            self.dodge = 0 + self.stat_agility * 0.1
            self.poison_acc = 0.0
            self.poisoned = 0.0
            self.item = [
                None, None, None,
                None, None, None,
                None, None, None,
            ]
            self.x, self.y = 30, 89

            import stage1_1
            game_framework.change_mode(stage1_1)

    def draw(self):
        self.state_machine.draw()
        if drawing_bb.draw_bb:
            draw_rectangle(*self.get_bb())
        #체력 바
        if self.poisoned == 0:
            draw_rectangle(37, 20, 37 + 100 * self.hp / self.max_hp, 30, 255, 0, 0, filled=True)
            draw_rectangle(36, 19, 138, 31)
        else:
            draw_rectangle(37, 20, 37 + 100 * self.hp / self.max_hp, 30, 0, 255, 0, filled=True)
            draw_rectangle(36, 19, 138, 31)
        #경험치 바
        draw_rectangle(37, 7, 37 + 100 * self.exp / self.next_level_exp, 17, 255, 255, 0, filled=True)
        draw_rectangle(36, 6, 138, 18, 255, 255, 0)
        # 레벨 표시
        self.level_image.clip_draw(0, 0, 35, 35, 20, 19)
        # 레벨 숫자 표시
        self.font.draw(8, 20, f'{self.level}', (0, 0, 0))
        # 회색곰 스킬1
        if grey_bear_skill1 != 0:
            image1 = load_image('grey_bear_skill1.png')
            image1.clip_draw(0, 0, 91, 70, self.x, self.y-30)
        # 회색곰 스킬2
        if grey_bear_skill2 != 0:
            image2 = load_image('grey_bear_skill2.png')
            if self.face_dir == 1:
                image2.clip_composite_draw(0, 0, 33, 98, 0, 'h', self.x + 10, self.y)
            else:
                image2.clip_draw(0, 0, 33, 98, self.x - 10, self.y)

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
                    self.y = int(self.y)
                    if self.y >= other.y + 50:
                        self.y = other.y + 60
                        self.yv = 0
                    else:
                        pass

        if group == 'char:monster':
            if self.immune_time == 0:
                self.immune_time = 0.5
                #print('player hit')
                defence = self.defense
                if defence > 80:
                    defence = 80
                damage = other.attack * ((100 - defence) / 100)
                if self.dodge >= random.randint(1, 100):
                    #print('dodge')
                    pass
                else:
                    self.hp -= damage
                    #print(f'player hp: {self.hp}/{self.max_hp}')

                if other.name == 'grey_bear':
                    chance1 = random.randint(1, 100)
                    chance2 = random.randint(1, 100)
                    global grey_bear_skill1
                    global grey_bear_skill2
                    if chance1 <= 10 and grey_bear_skill1 == 0:
                        self.hp -= 3 * ((100 - self.defense) / 100)
                        grey_bear_skill1 = get_time()
                        # print('1')
                    if chance2 <= 5:
                        self.hp -= 1 * ((100 - self.defense) / 100)
                        other.hp += 10
                        if other.hp > 300:
                            other.hp = 300
                        grey_bear_skill2 = get_time()
                        # print('2')

                if other.name == 'big_slime':
                    chance = random.randint(1, 100)
                    if chance <= 25 and self.poisoned == 0:
                        self.poisoned = 3.0

            if other.name == 'apple':
                self.hp += 10

            if other.name == 'golden_apple':
                self.hp += 50

def update_items():
    if not character_state.char is None:
        char = character_state.char

        char.item_max_hp = 0
        char.item_damage = 0
        char.item_attack = 0
        char.item_defense = 0
        char.item_speed = 0
        char.item_crit_chance = 0
        char.item_dodge = 0
        char.item_gold_bonus = 0

        for i in range(0, 9):
            if char.item[i] is not None:
                char.item_max_hp += char.item[i][1]
                char.item_damage += char.item[i][2]
                char.item_attack += char.item[i][3]
                char.item_defense += char.item[i][4]
                char.item_speed += char.item[i][5]
                char.item_dodge += char.item[i][6]
                char.item_crit_chance += char.item[i][7]

                if char.item[i][0] == 'Bronze_neko':
                    char.item_max_hp += char.gold * 0.001
                    char.item_attack += char.gold * 0.001
                    char.item_defense += char.gold * 0.001
                elif char.item[i][0] == 'Silver_neko':
                    char.item_max_hp += char.gold * 0.005
                    char.item_attack += char.gold * 0.005
                    char.item_defense += char.gold * 0.005
                elif char.item[i][0] == 'Gold_neko':
                    char.item_max_hp += char.gold * 0.01
                    char.item_attack += char.gold * 0.01
                    char.item_defense += char.gold * 0.01
                elif char.item[i][0] == 'Speed_boots':
                    char.item_attack += char.speed * 0.1
                elif char.item[i][0] == 'Magic_sword':
                    char.item_damage += char.attack * 0.1
                elif char.item[i][0] == 'Red_banner':
                    from stage import monster_count
                    char.item_attack += monster_count * 4
                elif char.item[i][0] == 'Yellow_banner':
                    from stage import monster_count
                    char.item_crit_chance += monster_count * 2
                elif char.item[i][0] == 'Blue_banner':
                    from stage import monster_count
                    char.item_defense += monster_count * 1
                elif char.item[i][0] == 'Green_banner':
                    from stage import monster_count
                    char.item_max_hp += monster_count * 3
                elif char.item[i][0] == 'Gold_ingot':
                    char.item_gold_bonus += 20

        char.max_hp = 100 + char.stat_hp * 1 + char.item_max_hp
        char.damage = 2 + char.stat_attack * 0.05 + char.item_damage
        char.attack = 100 + char.item_attack
        char.defense = 0 + char.stat_defense * 0.5 + char.item_defense
        char.speed = 100 + char.stat_agility * 1 + char.item_speed
        char.dodge = 0 + char.stat_agility * 0.1 + char.item_dodge
        char.crit_chance = 0 + char.stat_luck * 1 + char.item_crit_chance
        char.gold_bonus = char.item_gold_bonus


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
        if mouse_L_down(e) and not self.char.attacking or l_down(e) and not self.char.attacking:
            self.char.flame = 0
            self.char.attacking = True
            global attack
            attack = Attack(self.char)
            game_world.add_object(attack, 0)
            game_world.add_collision_pair('attack:monster', attack, None)
        if e_down(e):
               game_framework.push_mode(inventory_mode)
        if s_down(e):
            drawing_bb.draw_bb = not drawing_bb.draw_bb

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
        if mouse_L_down(e) and not self.char.attacking or l_down(e) and not self.char.attacking:
            self.char.flame = 0
            self.char.attacking = True
            global attack
            attack = Attack(self.char)
            game_world.add_object(attack, 1)
            game_world.add_collision_pair('attack:monster', attack, None)
        if e_down(e):
            game_framework.push_mode(inventory_mode)
        if s_down(e):
            drawing_bb.draw_bb = not drawing_bb.draw_bb

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

    def do(self):
        pass

    def get_bb(self):
        if self.char.face_dir == 1:
            return self.char.x + 10, self.char.y - 40, self.char.x + 42, self.char.y + 5
        else:
            return self.char.x - 42, self.char.y - 40, self.char.x - 10, self.char.y + 5

    def draw(self):
        if drawing_bb.draw_bb:
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

def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def l_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l

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
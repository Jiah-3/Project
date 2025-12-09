import random

from pico2d import load_image, draw_rectangle, load_font

import game_framework
import game_world
import stage
import drawing_bb

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

slime_skill3_cooldown = 150.0
slime_skill3_active = 0.0
slime_skill3_frame = 0

class Monster:
    def __init__(self):
        self.moving = 300
        self.image = load_image('test.png')
        self.x, self.y = 0, 0
        self.frame = 0
        self.max_frame = 0
        self.direction = 1
        self.move = 0
        self.size_x1 = 0
        self.size_y1 = 0
        self.size_x2 = 0
        self.size_y2 = 0
        self.name = None
        self.price = 0
        self.font = load_font('ENCR10B.TTF', 20)

        self.max_hp = 0
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.gold = 0
        self.exp = 0

        self.immune_time = 0.0

    def update(self):
        if self.immune_time > 0.0:
            self.immune_time -= game_framework.frame_time
            if self.immune_time < 0.0:
                self.immune_time = 0.0

        self.frame = (self.frame + FRAMES_PER_SEC * game_framework.frame_time / 3) % self.max_frame
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

        if self.x - self.size_x1 < 0:
            self.x = self.size_x1 + 20
            self.move = 1
        elif self.x + self.size_x2 > 800:
            self.x = 800 - self.size_x2 - 20
            self.move = -1

        if self.name == 'grey_bear' or self.name == 'big_slime':
            import character_state
            if not character_state.char == None:
                char = character_state.char
                if char.x < self.x:
                    self.direction = -1
                    self.move = -1
                else:
                    self.direction = 1
                    self.move = 1

        if self.name == 'big_slime':
            global slime_skill3_cooldown, slime_skill3_active, slime_skill3_frame
            if slime_skill3_cooldown > 0.0:
                slime_skill3_cooldown -= game_framework.frame_time
                if slime_skill3_active > 0.0:
                    slime_skill3_active -= game_framework.frame_time
                    slime_skill3_frame = (slime_skill3_frame + FRAMES_PER_SEC * game_framework.frame_time / 3) % 3

                if slime_skill3_cooldown < 0.0:
                    self.hp += (self.max_hp - self. hp) * 0.2
                    slime_skill3_active = 1.0
                    slime_skill3_cooldown = 150.0

    def draw(self):
        if self.name == 'big_slime':
            global slime_skill3_active, slime_skill3_frame
            if slime_skill3_active > 0:
                image = load_image('slime_skill3_effect.png')
                image.clip_draw(int(slime_skill3_frame) * 200, 0, 200, 200, self.x - 20, self.y - 10, 240, 240)
            if self.direction == 1:
                self.image.clip_draw(int(self.frame) * 200, 0, 200, 200, self.x, self.y)
            else:
                self.image.clip_composite_draw(int(self.frame) * 200, 0, 200, 200, 0, 'h', self.x, self.y, 200, 200)
        elif self.name == 'small_slime':
            if self.direction == 1:
                self.image.clip_draw(int(self.frame) * 50, 0, 50, 50, self.x, self.y)
            else:
                self.image.clip_composite_draw(int(self.frame) * 50, 0, 50, 50, 0, 'h', self.x, self.y, 50, 50)
        elif self.name == 'flame_god':
            if self.direction == 1:
                self.image.clip_draw(int(self.frame) * 120, 0, 120, 120, self.x, self.y)
            else:
                self.image.clip_composite_draw(int(self.frame) * 120, 0, 120, 120, 0, 'h', self.x, self.y, 120, 120)
        elif self.name == 'apple' or self.name == 'golden_apple':
            self.image.clip_draw(int(self.frame) * 30, 0, 30, 30, self.x, self.y)
        elif self.name == 'selling_tier3' or self.name == 'selling_tier2' or self.name == 'selling_tier1' or self.name == 'selling_heart':
            self.image.clip_draw(int(self.frame) * 120, 0, 120, 100, self.x, self.y)
        else:
            if self.direction == 1:
                self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
            else:
                self.image.clip_composite_draw(int(self.frame) * 100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)

        if drawing_bb.draw_bb:
            draw_rectangle(*self.get_bb())
        if self.name != 'apple' and self.name != 'golden_apple' and self.name != 'selling_tier3' and self.name != 'selling_tier2' and self.name != 'selling_tier1' and self.name != 'selling_heart':
            draw_rectangle(self.x - self.size_x1, self.y + self.size_y2, self.x - self.size_x1 + 100 * self.hp / self.max_hp, self.y + self.size_y2 + 10, 255, 0, 0, filled=True)
            draw_rectangle(self.x - self.size_x1, self.y + self.size_y2, self.x - self.size_x1 + 100, self.y + self.size_y2 + 10, 0, 0, 0)
        if self.name == 'selling_tier3' or self.name == 'selling_tier2' or self.name == 'selling_tier1' or self.name == 'selling_heart':
            self.font.draw(self.x - 50, self.y + 65, f'Price: {self.price}G', (255, 255, 0))



    def do(self):
        pass

    def get_bb(self):
        return self.x - self.size_x1, self.y - self.size_y1, self.x + self.size_x2, self.y + self.size_y2

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            #game_world.remove_object(self)
            if self.immune_time == 0:
                self.immune_time = 0.5
                #print('monster hit')
                if other.char.crit_chance >= random.randint(1, 100):
                    if other.char.crit_chance > 100:
                        crit_damage = (other.char.crit_chance - 100) / 100
                    else:
                        crit_damage = 0
                    damage = other.char.damage * 1.5 + (crit_damage) * (other.char.attack / 100) * ((100 - self.defense) / 100)
                    #print('critical hit')
                else:
                    damage = other.char.damage * (other.char.attack / 100) * ((100 - self.defense) / 100)
                if self.name == 'small_slime':
                    damage = 1
                self.hp -= damage
                #print(f'monster hp: {self.hp}/{self.max_hp}')

                if self.name == 'grey_bear':
                    pass

                if self.name == 'big_slime':
                    chance2 = random.randint(1, 100)
                    if chance2 <= 10:
                        _monster = Monster()
                        _monster.x = self.x
                        _monster.y = self.y - 75
                        game_world.add_object(_monster, 2)
                        _monster.set_size(25, 25, 25, 10)
                        _monster.set_stat(4, 1, 0, 50, 0, 0)
                        _monster.set_image('small_slime.png')
                        _monster.set_max_frame(2)
                        _monster.set_name('small_slime')
                        stage.monster_count += 1
                        game_world.add_collision_pair('attack:monster', None, _monster)
                        game_world.add_collision_pair('char:monster', None, _monster)
                        game_world.add_collision_pair('monster:block', _monster, None)

                if self.hp <= 0:
                    drop_chance = random.randint(1, 100)
                    if self.name != 'small_slime' and self.name != 'selling_tier3' and self.name != 'selling_tier2' and self.name != 'selling_tier1' and self.name != 'selling_heart':
                        if drop_chance <= 10:
                            apple = Monster()
                            apple.x = self.x
                            apple.y = self.y - 35
                            game_world.add_object(apple, 2)
                            apple.set_size(10, 15, 10, 10)
                            apple.set_stat(1, 0, 0, 0, 0, 0)
                            apple.set_image('apple.png')
                            apple.set_max_frame(1)
                            apple.set_name('apple')
                            game_world.add_collision_pair('char:monster', None, apple)
                        elif drop_chance == 11:
                            apple = Monster()
                            apple.x = self.x
                            apple.y = self.y - 35
                            game_world.add_object(apple, 2)
                            apple.set_size(10, 15, 10, 10)
                            apple.set_stat(1, 0, 0, 0, 0, 0)
                            apple.set_image('golden_apple.png')
                            apple.set_max_frame(1)
                            apple.set_name('golden_apple')
                            game_world.add_collision_pair('char:monster', None, apple)
                    if self.name == 'selling_tier3' or self.name == 'selling_tier2' or self.name == 'selling_tier1' or self.name == 'selling_heart':
                        if other.char.gold >= self.price:
                            for i in range(0, 9):
                                if other.char.item[i] == None:
                                    other.char.gold -= self.price
                                    from reward import set_item
                                    if self.name == 'selling_tier3':
                                        game_world.remove_object(self)
                                        set_item(3)
                                    elif self.name == 'selling_tier2':
                                        game_world.remove_object(self)
                                        set_item(2)
                                    elif self.name == 'selling_tier1':
                                        game_world.remove_object(self)
                                        set_item(1)
                                    break
                            else:
                                self.hp = 1
                            if self.name == 'selling_heart':
                                game_world.remove_object(self)
                                other.char.hp += int(other.char.max_hp * 0.2)


                    else:
                        game_world.remove_object(self)
                        other.char.gold += self.gold * (100 + other.char.gold_bonus) / 100
                        other.char.exp += self.exp
                        stage.monster_count -= 1
        if group == 'monster:block':
            self.direction = self.direction * -1
            self.move = self.move * -1
            self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time * self.speed / 100

        if group == 'char:monster':
            if self.name == 'apple' or self.name == 'golden_apple':
                game_world.remove_object(self)


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

    def set_name(self, name):
        self.name = name

    def set_image(self, image):
        self.image = load_image(image)

    def set_max_frame(self, frame):
        self.max_frame = frame
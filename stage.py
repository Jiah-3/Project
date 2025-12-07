from random import randint

from pico2d import load_image, draw_rectangle

import character_state
import game_world
from background import Bg
import drawing_bb
from monster import Monster

monster_count = 0

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        self.x, self.y = 0, 0
        self.width = 50

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        if drawing_bb.draw_bb:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y + 9, self.x + 50, self.y + 10

    def set_ground(self, stage):
        if stage == 1:
            self.image = load_image('ground.png')
        elif stage == 2:
            self.image = load_image('ground2.png')

    def handle_collision(self, group, other):
        if group == 'char:ground':
            pass

class Block:
    def __init__(self):
        self.x = 50
        self.y = 50

    def update(self):
        pass

    def draw(self):
        if drawing_bb.draw_bb:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'monster:block':
            pass

positions = []

def set_shop():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        if character_state.char.stage == '2_3' or character_state.char.stage == '2_6' or character_state.char.stage == '2_9' or character_state.char.stage == '2_10':
            ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    if character_state.char.stage == '2_3' or character_state.char.stage == '2_6' or character_state.char.stage == '2_9' or character_state.char.stage == '2_10':
        bg.set_bg(2)
    else:
        bg.set_bg(1)
    game_world.add_object(bg, 0)
    #상점 소환
    monster_positions = [(250, 90), (400, 90), (550, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_stat(1, 0, 0, 0, 0, 0)

        selling = randint(1, 8)
        if selling <= 3: # 3티어 상자
            monster.set_size(60, 50, 60, 50)
            monster.set_image('selling_tier3.png')
            monster.set_max_frame(1)
            monster.set_name('selling_tier3')
            monster.price = 100
            game_world.add_collision_pair('attack:monster', None, monster)
            game_world.add_collision_pair('char:monster', None, monster)
            game_world.add_collision_pair('monster:block', monster, None)
        elif selling <= 5: # 2티어 상자
            monster.set_size(60, 50, 60, 50)
            monster.set_image('selling_tier2.png')
            monster.set_max_frame(1)
            monster.set_name('selling_tier2')
            monster.price = 300
            game_world.add_collision_pair('attack:monster', None, monster)
            game_world.add_collision_pair('char:monster', None, monster)
            game_world.add_collision_pair('monster:block', monster, None)
        elif selling <= 6: # 1티어 상자
            monster.set_size(60, 50, 60, 50)
            monster.set_image('selling_tier1.png')
            monster.set_max_frame(1)
            monster.set_name('selling_tier1')
            monster.price = 500
            game_world.add_collision_pair('attack:monster', None, monster)
            game_world.add_collision_pair('char:monster', None, monster)
            game_world.add_collision_pair('monster:block', monster, None)
        elif selling <= 8: # 체력 회복 포션
            monster.set_size(50, 50, 50, 50)
            monster.set_image('selling_heart.png')
            monster.set_max_frame(1)
            monster.set_name('selling_heart')
            monster.price = 200
            game_world.add_collision_pair('attack:monster', None, monster)
            game_world.add_collision_pair('char:monster', None, monster)
            game_world.add_collision_pair('monster:block', monster, None)

def set_stage1_1():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    #뱀 소환
    monster_positions = [(300, 90), (400, 90), (500, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 16)
        monster.set_stat(20, 3, 0, 60, 10, 0.25)
        monster.set_image('snake.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = []
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_2():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),

                 (150, 130), (250, 130),
                 (550, 130), (650, 130),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 뱀 소환
    monster_positions = [(300, 90), (200, 190), (500, 90), (600, 190), (350, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 16)
        monster.set_stat(20, 3, 0, 60, 10, 0.25)
        monster.set_image('snake.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(70, 190), (330, 190), (470, 190), (730, 190)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)

def set_stage1_3():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),

                 (250, 130), (350, 130), (450, 130), (550, 130),
                 (150, 230), (250, 230), (550, 230), (650, 230),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 뱀 소환
    monster_positions = [(300, 190), (400, 190), (500, 190)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 16)
        monster.set_stat(20, 3, 0, 60, 10, 0.25)
        monster.set_image('snake.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 늑대 소환
    monster_positions = [(200, 290), (600, 290), (200, 90), (350, 90), (450, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 16)
        monster.set_stat(25, 5, 2, 70, 15, 0.5)
        monster.set_image('wolf.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(170, 190), (630, 190), (70, 290), (330, 290), (470, 290), (730, 290)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)

def set_stage1_4():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),

                 (50, 130), (150, 130), (650, 130), (750, 130),
                 (50, 230), (150, 230), (650, 230), (750, 230),

                 (120, 330), (200, 330),
                 (300, 330), (400, 330), (500, 330),
                 (600, 330), (680, 330),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 늑대 소환
    monster_positions = [(200, 390), (320, 390), (400, 390), (50, 290), (650, 190), (270, 90), (390, 90), (500, 90),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 16)
        monster.set_stat(25, 5, 2, 70, 15, 0.5)
        monster.set_image('wolf.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(40, 390), (760, 390), (230, 290), (570, 290), (230, 190), (570, 190)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_5():
    global positions
    positions = [(0, 30), (50, 30), (250, 30), (300, 30),
                 (500, 30), (550, 30), (750, 30),

                 (50, 230), (150, 230), (350, 230), (450, 230), (650, 230), (750, 230),

                 (200, 430), (300, 430), (400, 430), (500, 430), (600, 430),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 늑대 소환
    monster_positions = [(90, 290), (110, 290), (690, 290), (710, 290), (500, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 16)
        monster.set_stat(25, 5, 2, 70, 15, 0.5)
        monster.set_image('wolf.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 엔트 소환
    monster_positions = [(300, 490), (370, 490), (520, 490), (400, 290), (275, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 36)
        monster.set_stat(50, 4, 5, 30, 18, 0.8)
        monster.set_image('ent.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [
        (130, 90), (170, 90), (380, 90), (420, 90), (630, 90), (670, 90),
        (230, 290), (270, 290), (530, 290), (570, 290),
        (120, 490), (680, 490)
                      ]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_6():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 회색곰 소환
    monster_positions = [(300, 90),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 40)
        monster.set_stat(300, 10, 10, 70, 300, 10)
        monster.set_image('grey_bear.png')
        monster.set_max_frame(2)
        monster.set_name('grey_bear')
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
def set_stage1_7():
    global positions
    positions = [
        (0, 30), (100, 30), (200, 30), (300, 30), (400, 30),
        (500, 30), (600, 30), (700, 30), (800, 30),

        (100, 130), (200, 130), (600, 130), (700, 130), (400, 230), (500, 230), (200, 330), (300, 330), (400, 330)
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)
    # 엔트 소환
    monster_positions = [(210, 90), (320, 90), (540, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 36)
        monster.set_stat(50, 4, 5, 30, 18, 0.8)
        monster.set_image('ent.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 슬라임 소환
    monster_positions = [(150, 190), (650, 190), (450, 290), (250, 390), (350, 390)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 30)
        monster.set_stat(40, 5, 3, 80, 20, 1)
        monster.set_image('slime.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(20, 190), (280, 190), (520, 190), (780, 190), (320, 290), (580, 290), (120, 390), (480, 390)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_8():
    global positions
    positions = [
        (0, 30), (100, 30), (200, 30), (300, 30), (400, 30),
        (500, 30), (600, 30), (650, 30),

        (150, 230), (200, 230), (300, 230), (400, 230),
        (500, 230), (600, 230), (700, 230), (800, 230),

        (0, 430), (100, 430), (200, 430), (300, 430), (400, 430),
        (500, 430), (600, 430), (650, 430),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)
    # 늑대 소환
    monster_positions = [(200, 90), (300, 90), (400, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 16)
        monster.set_stat(25, 5, 2, 70, 15, 0.5)
        monster.set_image('wolf.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 엔트 소환
    monster_positions = [(320, 290), (420, 290), (520, 290)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 36)
        monster.set_stat(50, 4, 5, 30, 18, 0.8)
        monster.set_image('ent.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 슬라임 소환
    monster_positions = [(160, 490), (260, 490), (360, 490)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 30)
        monster.set_stat(40, 5, 3, 80, 20, 1)
        monster.set_image('slime.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(730, 90), (70, 290), (730, 490)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_9():
    global positions
    positions = [
        (0, 30), (100, 30), (200, 30), (300, 30),
        (500, 30), (600, 30), (700, 30), (800, 30),

        (0, 230), (100, 230), (200, 230), (300, 230),
        (500, 230), (600, 230), (700, 230), (800, 230),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)
    # 슬라임 소환
    monster_positions = [(250, 90), (50, 290), (150, 290), (250, 290), (550, 90), (650, 90), (750, 90), (550, 290), (650, 290), (750, 290)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(45, 50, 45, 30)
        monster.set_stat(40, 5, 3, 80, 20, 1)
        monster.set_image('slime.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(380, 90), (420, 90), (380, 290), (420, 290)]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage1_10():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(1)
    game_world.add_object(bg, 0)

    # 빅슬라임 소환
    monster_positions = [(600, 90), ]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(100, 100, 100, 30)
        monster.set_stat(500, 3, 15, 85, 500, 20)
        monster.set_image('big_slime.png')
        monster.set_max_frame(3)
        monster.set_name('big_slime')
        monster.y += 50
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
def set_stage2_1():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 미라 소환
    monster_positions = [(400, 90), (500, 90), (600, 90), (300, 90), (700, 90)]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 40)
        monster.set_stat(80, 7, 10, 60, 20, 2)
        monster.set_image('mirra.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
def set_stage2_2():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),

                 (300, 130), (400, 130), (500, 130), (600, 130),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 미라 소환
    monster_positions = [(400, 90), (500, 90), (600, 90), (300, 90),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 40)
        monster.set_stat(80, 7, 10, 60, 20, 2)
        monster.set_image('mirra.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 트롤 소환
    monster_positions = [(400, 190), (500, 190),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(200, 10, 5, 40, 25, 4)
        monster.set_image('troll.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(220, 190), (680, 190),]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage2_3():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (600, 30), (700, 30), (800, 30),

                 (200, 230), (300, 230), (400, 230), (500, 230), (600, 230),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 미라 소환
    monster_positions = [(150, 90), (650, 90), (750, 90),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 40)
        monster.set_stat(80, 7, 10, 60, 20, 2)
        monster.set_image('mirra.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 트롤 소환
    monster_positions = [(250, 290), (340, 290), (470, 290), (520, 290),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(200, 10, 5, 40, 25, 4)
        monster.set_image('troll.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [(280, 90), (520, 90), (120, 290), (680, 290),]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage2_4():
    global positions
    positions = [(0, 30), (50, 30), (250, 30), (350, 30),
                 (450, 30), (550, 30), (750, 30),

                 (50, 230), (150, 230), (350, 230), (450, 230), (650, 230), (750, 230),

                 (200, 430), (300, 430), (400, 430), (500, 430), (600, 430),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 트롤 소환
    monster_positions = [(300, 90), (400, 90), (100, 290), (320, 490),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(200, 10, 5, 40, 25, 4)
        monster.set_image('troll.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 골렘 소환
    monster_positions = [(400, 290), (700, 290), (430, 490),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(150, 8, 30, 30, 30, 6)
        monster.set_image('golem.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [
        (130, 90), (170, 90), (630, 90), (670, 90),
        (230, 290), (270, 290), (530, 290), (570, 290),
        (120, 490), (680, 490)
                      ]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage2_5():
    global positions
    positions = [(50, 30), (150, 30), (650, 30), (750, 30),

    (150, 130), (250, 130), (350, 130), (450, 130), (550, 130), (650, 130),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 골렘 소환
    monster_positions = [(270, 190), (330, 190), (480, 190), (520, 190), (590, 190),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(150, 8, 30, 30, 30, 6)
        monster.set_image('golem.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [
        (70, 190), (730, 190), ]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def set_stage2_6():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 스콜피온 소환
    monster_positions = [(300, 90),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(47, 50, 47, 40)
        monster.set_stat(700, 20, 15, 90, 400, 50)
        monster.set_image('scorpion.png')
        monster.set_max_frame(2)
        monster.set_name('scorpion')
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
def set_stage2_7():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (300, 30), (400, 30), (500, 30),
                 (600, 30), (700, 30), (800, 30),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 미라 소환
    monster_positions = [
        (400, 90), (500, 90), (600, 90), (300, 90), (700, 90),
                         (450, 90), (550, 90), (650, 90), (350, 90), (750, 90),
    ]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(35, 50, 35, 40)
        monster.set_stat(80, 7, 10, 60, 20, 2)
        monster.set_image('mirra.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
def set_stage2_8():
    global positions
    positions = [(0, 30), (100, 30), (200, 30),
                 (600, 30), (700, 30), (800, 30),

                (200, 130), (300, 130), (400, 130), (500, 130), (600, 130),
                (100, 230),(200, 230), (300, 230), (400, 230), (500, 230), (600, 230), (700, 230),
                 ]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
        ground.set_ground(2)
        game_world.add_object(ground, 1)
        game_world.add_collision_pair('char:ground', None, ground)
    bg = Bg()
    bg.set_bg(2)
    game_world.add_object(bg, 0)

    # 트롤 소환
    monster_positions = [(350, 190), (450, 190), (550, 190),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(200, 10, 5, 40, 25, 4)
        monster.set_image('troll.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    # 미노타우르스 소환
    monster_positions = [(200, 290), (400, 290), (600, 290),]
    monsters = [Monster() for _ in monster_positions]
    for monster, (x, y) in zip(monsters, monster_positions):
        monster.x = x
        monster.y = y
        game_world.add_object(monster, 2)
        monster.set_size(50, 50, 50, 20)
        monster.set_stat(100, 15, 8, 80, 50, 8)
        monster.set_image('minotaurs.png')
        monster.set_max_frame(2)
        game_world.add_collision_pair('attack:monster', None, monster)
        game_world.add_collision_pair('char:monster', None, monster)
        game_world.add_collision_pair('monster:block', monster, None)
    #벽 생성
    block_position = [
        (280, 90), (520, 90),
        (120, 190), (680, 190),
        (20, 290), (780, 290),
    ]
    blocks = [Block() for _ in block_position]
    for block, (x, y) in zip(blocks, block_position):
        block.x = x
        block.y = y
        game_world.add_object(block, 0)
        game_world.add_collision_pair('monster:block', None, block)
def get_ground_positions():
    return positions

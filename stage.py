from pico2d import load_image, draw_rectangle

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
        return self.x - 50, self.y - 30, self.x + 50, self.y + 10

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
        monster.set_stat(20, 3, 0, 60, 10, 0.1)
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
        monster.set_stat(20, 3, 0, 60, 10, 0.1)
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
        monster.set_stat(20, 3, 0, 60, 10, 0.1)
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
        monster.set_stat(25, 5, 2, 70, 15, 0.25)
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

def get_ground_positions():
    return positions

from random import randint

from pico2d import *

import character_state
import game_framework
import game_world
import stage
from character import Char

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPH = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPH / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 9.8  # 중력 가속도 (m/s²)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3
FRAMES_PER_SEC = FRAMES_PER_ACTION * ACTION_PER_TIME

image = None
frame = 0
tier = 0
item = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            if stage.monster_count == -1:
                game_framework.pop_mode()
        else:
            char.handle_event(event)

def finish():
    character_state.char = char
    game_world.collision_pairs.clear()
    game_world.clear()

def init():
    global char
    global tier
    global image
    global frame

    frame = 0
    set_tier()

    char = Char()
    if character_state.char != None:
        char = character_state.char

def update():
    game_world.update()
    game_world.handle_collisions()

    global frame
    if int(frame) != 9:
        frame = (frame + FRAMES_PER_SEC * game_framework.frame_time) % 10
    elif int(frame) == 9 and stage.monster_count == 0:
        stage.monster_count -= 1
        set_item()

def draw():
    clear_canvas()
    game_world.render()
    image.clip_draw(int(frame) * 120, 0, 120, 100, 400, 300)
    if stage.monster_count == -1:
        global item
        if item[8] is not None:
            item_image = load_image(item[8])
            item_image.draw(400, 350)
    update_canvas()

def pause():
    pass

def resume():
    pass

def set_tier():
    global tier, image
    tier_rate = randint(1, 100)
    if tier_rate <= 60:
        tier = 3
        image = load_image("tier3.png")
    elif tier_rate <= 90:
        tier = 2
        image = load_image("tier2.png")
    else:
        tier = 1
        image = load_image("tier1.png")

    if character_state.char.stage == '1_6' or character_state.char.stage == '1_10':
        tier = 1
        image = load_image("tier1.png")

def set_item():
    if tier == 1: # 10% rare ~ mythic
        item_rate = randint(1, 19)
        if item_rate <= 10: # rare
            pass
        elif item_rate <= 15: # legendary
            pass
        elif item_rate <= 18: # fabled
            pass
        elif item_rate == 19: # mythic
            pass

    elif tier == 2: # 30% unique ~ mythic
        item_rate = randint(1, 49)
        if item_rate <= 30: # unique
            pass
        elif item_rate <= 40: # rare
            pass
        elif item_rate <= 45: # legendary
            pass
        elif item_rate <= 48: # fabled
            pass
        elif item_rate == 49: # mythic
            pass

    elif tier == 3: # 60% common ~ mythic
        item_rate = randint(1, 100)
        if item_rate <= 100: # common
            from item import common
            global item
            item = common[randint(0, len(common)-1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    break
            pass
        elif item_rate <= 81: # unique
            pass
        elif item_rate <= 91: # rare
            pass
        elif item_rate <= 96: # legendary
            pass
        elif item_rate <= 99: # fabled
            pass
        elif item_rate == 100: # mythic
            pass
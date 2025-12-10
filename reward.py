from random import randint

from pico2d import *

import character_state
import game_framework
import game_world
import stage
from character import Char
from play_music import play_reward

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
font = None

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
    global char, image, frame, tier, font

    frame = 0
    set_tier()
    font = load_font('ENCR10B.TTF', 20)

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
        play_reward()

def draw():
    clear_canvas()
    game_world.render()
    image.clip_draw(int(frame) * 120, 0, 120, 100, 400, 300)
    if stage.monster_count == -1:
        global item, font
        if item[8] is not None:
            item_image = load_image(item[8])
            item_image.draw(400, 350)
            # font.draw(350, 380, f'{item[9]}!', (0, 0, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass

def set_tier(Tier=0):
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

    if character_state.char.stage == '1_6' or character_state.char.stage == '1_10' or character_state.char.stage == '2_6' or character_state.char.stage == '2_10':
        tier = 1
        image = load_image("tier1.png")
    if Tier != 0:
        tier = Tier
        image = load_image(f"tier{Tier}.png")

def set_item(Tier = 0):
    global item, tier
    if Tier != 0:
        tier = Tier
    if tier == 1: # 10% rare ~ mythic
        item_rate = randint(1, 19)
        if item_rate <= 10: # rare
            from item import rare
            item = rare[randint(0, len(rare) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
            else:
                if item[10] == 6:
                    character_state.char.gold += 100
                elif item[10] == 5:
                    character_state.char.gold += 300
                elif item[10] == 4:
                    character_state.char.gold += 500
                elif item[10] == 3:
                    character_state.char.gold += 800
                elif item[10] == 2:
                    character_state.char.gold += 1000
                elif item[10] == 1:
                    character_state.char.gold += 1500
        elif item_rate <= 15: # legendary
            from item import legendary
            item = legendary[randint(0, len(legendary) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 18: # fabled
            from item import fabled
            item = fabled[randint(0, len(fabled) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate == 19: # mythic
            from item import mythic
            item = mythic[randint(0, len(mythic)-1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break

    elif tier == 2: # 30% unique ~ mythic
        item_rate = randint(1, 49)
        if item_rate <= 30: # unique
            from item import unique
            item = unique[randint(0, len(unique) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 40: # rare
            from item import rare
            item = rare[randint(0, len(rare) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 45: # legendary
            from item import legendary
            item = legendary[randint(0, len(legendary) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 48: # fabled
            from item import fabled
            item = fabled[randint(0, len(fabled) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate == 49: # mythic
            from item import mythic
            item = mythic[randint(0, len(mythic)-1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break

    elif tier == 3: # 60% common ~ mythic
        item_rate = randint(1, 100)
        if item_rate <= 51: # common
            from item import common
            item = common[randint(0, len(common)-1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 81: # unique
            from item import unique
            item = unique[randint(0, len(unique) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 91: # rare
            from item import rare
            item = rare[randint(0, len(rare) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 96: # legendary
            from item import legendary
            item = legendary[randint(0, len(legendary) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate <= 99: # fabled
            from item import fabled
            item = fabled[randint(0, len(fabled) - 1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
        elif item_rate == 100: # mythic
            from item import mythic
            item = mythic[randint(0, len(mythic)-1)]
            for i in range(0, 9):
                if character_state.char.item[i] is None:
                    character_state.char.item[i] = item
                    character_state.char.hp += item[1]
                    break
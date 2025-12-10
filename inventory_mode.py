from pico2d import *

import character
import character_state
import game_framework
import game_world
from inventory import Inventory

num = -1

def init():
    global inventory, num
    num = -1
    inventory = Inventory()
    game_world.add_object(inventory, 2)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            character_state.char.stat_hp += 10
            character_state.char.hp += 25
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            character_state.char.stat_attack += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            character_state.char.stat_defense += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            character_state.char.stat_agility += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            character_state.char.stat_luck += 10
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            event.y = 600 + event.y * -1
            global num
            num = -1
            if event.x >= 270 and event.x <= 350:
                num += 1
            elif event.x >= 360 and event.x <= 440:
                num += 2
            elif event.x >= 450 and event.x <= 530:
                num += 3
            if event.y <= 270 and event.y >= 190:
                pass
            elif event.y <= 180 and event.y >= 100:
                num += 3
            elif event.y <= 90 and event.y >= 10:
                num += 6
            if num != -1:
                if character_state.char.item[num] != None:
                    if character_state.char.item[num][10] == 6:
                        character_state.char.gold += 100
                    elif character_state.char.item[num][10] == 5:
                        character_state.char.gold += 300
                    elif character_state.char.item[num][10] == 4:
                        character_state.char.gold += 500
                    elif character_state.char.item[num][10] == 3:
                        character_state.char.gold += 800
                    elif character_state.char.item[num][10] == 2:
                        character_state.char.gold += 1000
                    elif character_state.char.item[num][10] == 1:
                        character_state.char.gold += 1500

                character_state.char.item[num] = None
                character.update_items()

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            event.y = 600 + event.y * -1
            if event.x >= 20 and event.x <= 170:
                global inventory
                if inventory.char.stat_points > 0:
                    if event.y <= 512 and event.y >= 482:
                        character_state.char.stat_hp += 1
                        character_state.char.max_hp += 2.5
                        character_state.char.hp += 2.5
                        character_state.char.stat_points -= 1
                    if event.y <= 462 and event.y >= 432:
                        character_state.char.stat_attack += 1
                        character_state.char.damage += 0.1
                        character_state.char.stat_points -= 1
                    if event.y <= 412 and event.y >= 382:
                        character_state.char.stat_defense += 1
                        character_state.char.defense += 0.5
                        character_state.char.stat_points -= 1
                    if event.y <= 362 and event.y >= 332:
                        character_state.char.stat_agility += 1
                        character_state.char.speed += 2
                        character_state.char.dodge += 0.25
                        character_state.char.stat_points -= 1
                    if event.y <= 312 and event.y >= 282:
                        character_state.char.stat_luck += 1
                        character_state.char.crit_chance += 1.5
                        character_state.char.stat_points -= 1

            num = -1
            if event.x >= 270 and event.x <= 350:
                num += 1
            elif event.x >= 360 and event.x <= 440:
                num += 2
            elif event.x >= 450 and event.x <= 530:
                num += 3
            if event.y <= 270 and event.y >= 190:
                pass
            elif event.y <= 180 and event.y >= 100:
                num += 3
            elif event.y <= 90 and event.y >= 10:
                num += 6
            # print(f"Left click at: ({event.x}, {event.y})")

def finish():
    global inventory
    game_world.remove_object(inventory)
    del inventory


def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    if num != -1 and character_state.char.item[num] != None:
        font = load_font('ENCR10B.TTF', 12)
        font.draw(240, 280, f'{character_state.char.item[num][9]}', (0, 0, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass
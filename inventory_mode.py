from pico2d import *

import character_state
import game_framework
import game_world
from inventory import Inventory

def init():
    global inventory
    inventory = Inventory()
    game_world.add_object(inventory, 2)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            event.y = 600 + event.y * -1
            if event.x >= 20 and event.x <= 170:
                global inventory
                if inventory.char.stat_points > 0:
                    if event.y <= 512 and event.y >= 482:
                        character_state.char.stat_hp += 1
                        character_state.char.max_hp += 1
                        character_state.char.hp += 1
                        character_state.char.stat_points -= 1

                    if event.y <= 462 and event.y >= 432:
                        character_state.char.stat_attack += 1
                        character_state.char.damage += 0.05
                        character_state.char.stat_points -= 1
                    if event.y <= 412 and event.y >= 382:
                        character_state.char.stat_defense += 1
                        character_state.char.defense += 0.5
                        character_state.char.stat_points -= 1
                    if event.y <= 362 and event.y >= 332:
                        character_state.char.stat_agility += 1
                        character_state.char.speed += 1
                        character_state.char.dodge += 0.1
                        character_state.char.stat_points -= 1
                    if event.y <= 312 and event.y >= 282:
                        character_state.char.stat_luck += 1
                        character_state.char.crit_chance += 1
                        character_state.char.stat_points -= 1

            print(f"Left click at: ({event.x}, {event.y})")

def finish():
    global inventory
    game_world.remove_object(inventory)
    del inventory


def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
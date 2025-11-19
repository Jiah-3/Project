from pico2d import *

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
from pico2d import *

import game_framework
import game_world
from character import Char
from stage import set_stage1_1


#class

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            char.handle_event(event)

def finish():
    game_world.clear()

def init():
    global char

    set_stage1_1()

    char = Char()
    game_world.add_object(char, 2)
    game_world.add_collision_pair('char:ground', char, None)

def update():
    game_world.update()
    game_world.handle_collisions()
    #print(char.y)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
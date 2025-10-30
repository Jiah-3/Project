from pico2d import *

import game_world
from character import Char
from ground import stage1_1


#class

def handle_events():
    global start

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            start = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            start = False
        else:
            char.handle_event(event)

def reset_world():
    global char

    stage1_1()

    char = Char()
    game_world.add_object(char, 1)

def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

start = True

open_canvas()
reset_world()

while start:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()
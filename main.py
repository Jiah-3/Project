from pico2d import *

from character import Char


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
    global world
    global char

    world = []

    char = Char()
    world.append(char)

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
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
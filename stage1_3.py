from pico2d import *

import character_state
import game_framework
import game_world
import stage
from character import Char

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            if stage.monster_count == 0:
                import shop
                game_framework.change_mode(shop)
                pass
        else:
            char.handle_event(event)

def finish():
    character_state.char = char
    game_world.collision_pairs.clear()
    game_world.clear()

def init():
    global char

    stage.set_stage1_3()
    stage.monster_count = 5

    char = Char()
    game_world.add_object(char, 2)
    game_world.add_collision_pair('char:ground', char, None)
    game_world.add_collision_pair('char:monster', char, None)

def update():
    game_world.update()
    game_world.handle_collisions()
    #print(char.y)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    character_state.char = char

def resume():
    pass
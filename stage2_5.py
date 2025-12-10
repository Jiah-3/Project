from pico2d import *

import character_state
import game_framework
import game_world
import reward
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
                game_framework.push_mode(reward)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            stage.monster_count = -1
        else:
            char.handle_event(event)

def finish():
    character_state.char = char
    game_world.collision_pairs.clear()
    game_world.clear()

def init():
    global char

    stage.set_stage2_5()
    stage.monster_count = 5

    char = Char()
    if character_state.char != None:
        char = character_state.char
        char.x = 30
        char.y = 90
        char.yv = 0
    char.stage = '2_5'
    game_world.add_object(char, 2)
    game_world.add_collision_pair('char:ground', char, None)
    game_world.add_collision_pair('char:monster', char, None)

def update():
    game_world.update()
    game_world.handle_collisions()
    if stage.monster_count == -1:
        import stage2_6
        game_framework.change_mode(stage2_6)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    character_state.char = char

def resume():
    pass
from pico2d import *

import character_state
import ending
import game_framework
import game_world
import reward
import stage
from character import Char
from play_music import stop_music, play_stage3


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            if stage.monster_count == 0:
                game_framework.push_mode(ending)
        else:
            char.handle_event(event)

def finish():
    character_state.char = char
    game_world.collision_pairs.clear()
    game_world.clear()
    stop_music()

def init():
    global char

    stage.set_stage3_1()
    stage.monster_count = 1

    char = Char()
    if character_state.char != None:
        char = character_state.char
        char.x = 30
        char.y = 90
        char.yv = 0
    char.stage = '3_1'
    game_world.add_object(char, 2)
    game_world.add_collision_pair('char:ground', char, None)
    game_world.add_collision_pair('char:monster', char, None)
    stop_music()
    play_stage3()

def update():
    game_world.update()
    game_world.handle_collisions()
    if stage.monster_count == -1:
        import shop
        game_framework.change_mode(shop)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    character_state.char = char

def resume():
    pass
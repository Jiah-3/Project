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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w or event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if stage.monster_count == 0:
                if char.stage == '1_3':
                    import stage1_4
                    game_framework.change_mode(stage1_4)
                elif char.stage == '1_6':
                    import stage1_7
                    game_framework.change_mode(stage1_7)
                elif char.stage == '1_9':
                    import stage1_10
                    game_framework.change_mode(stage1_10)
                elif char.stage == '1_10':
                    import stage2_1
                    game_framework.change_mode(stage2_1)
                elif char.stage == '2_3':
                    import stage2_4
                    game_framework.change_mode(stage2_4)
                elif char.stage == '2_6':
                    import stage2_7
                    game_framework.change_mode(stage2_7)
                elif char.stage == '2_9':
                    import stage2_10
                    game_framework.change_mode(stage2_10)
                elif char.stage == '2_10':
                    import stage3_1
                    game_framework.change_mode(stage3_1)
        else:
            char.handle_event(event)

def finish():
    character_state.char = char
    game_world.collision_pairs.clear()
    game_world.clear()

def init():
    global char

    stage.set_shop()
    stage.monster_count = 0

    char = Char()
    if character_state.char != None:
        char = character_state.char
        char.x = 30
        char.y = 90
        char.yv = 0
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
from pico2d import *
import game_framework
from play_music import stop_music, play_stage3, play_ending

image = None
font = None

def init():
    global image
    global font
    image = load_image('background1.png')
    font = load_font('ENCR10B.TTF', 60)
    stop_music()
    play_ending()

def finish():
    global image, font
    del image, font
    stop_music()

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    font.draw(120, 450, 'congratulations!', (255, 255, 153))
    update_canvas()

def handle_events():
    event_list = get_events() # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def pause():
    pass

def resume():
    pass
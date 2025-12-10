# python
from pico2d import *
import game_framework
import stage1_1

image = None
font = None
music = None

def init():
    global image, font, music
    image = load_image('title_image.png')
    font = load_font('ENCR10B.TTF', 40)
    # 음악 로드 및 반복 재생
    music = load_music('title.mp3')
    music.set_volume(64)      # 볼륨 조정 (0~100)
    music.repeat_play()       # 반복 재생

def finish():
    global image, font, music
    # 음악 정지 및 정리
    if music:
        music.stop()
        del music
    del image, font

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    font.draw(152, 102, 'Press Space to start', (0, 0, 0))
    font.draw(150, 100, 'Press Space to start', (204, 255, 153))
    update_canvas()

def handle_events():
    event_list = get_events() # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(stage1_1)

def pause():
    pass

def resume():
    pass
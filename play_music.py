from pico2d import load_music, load_wav

_music1 = None
_music2 = None
_music3 = None
_music4 = None
_music5 = None
_music6 = None
_music7 = None
_music8 = None

def play_stage1():
    global _music1
    if _music1 is None:
        _music1 = load_music('stage1.mp3')   # 파일명은 프로젝트에 맞게
        _music1.set_volume(30)               # 볼륨 조정(0~100)
    _music1.repeat_play()

def play_stage2():
    global _music2
    if _music2 is None:
        _music2 = load_music('stage2.mp3')   # 파일명은 프로젝트에 맞게
        _music2.set_volume(30)               # 볼륨 조정(0~100)
    _music2.repeat_play()

def play_stage3():
    global _music3
    if _music3 is None:
        _music3 = load_music('stage3.mp3')   # 파일명은 프로젝트에 맞게
        _music3.set_volume(30)               # 볼륨 조정(0~100)
    _music3.repeat_play()

def play_reward():
    global _music4
    if _music4 is None:
        _music4 = load_wav('reward.wav')   # 파일명은 프로젝트에 맞게
        _music4.set_volume(40)               # 볼륨 조정(0~100)
    _music4.play()

def play_ending():
    global _music5
    if _music5 is None:
        _music5 = load_music('ending.mp3')   # 파일명은 프로젝트에 맞게
        _music5.set_volume(30)               # 볼륨 조정(0~100)
    _music5.repeat_play()

def play_fireball():
    global _music6
    if _music6 is None:
        _music6 = load_wav('fireball.wav')   # 파일명은 프로젝트에 맞게
        _music6.set_volume(40)               # 볼륨 조정(0~100)
    _music6.play()

def play_boom():
    global _music7
    if _music7 is None:
        _music7 = load_wav('boom.wav')   # 파일명은 프로젝트에 맞게
        _music7.set_volume(100)               # 볼륨 조정(0~100)
    _music7.play()

def play_death():
    global _music8
    if _music8 is None:
        _music8 = load_wav('death.wav')   # 파일명은 프로젝트에 맞게
        _music8.set_volume(20)               # 볼륨 조정(0~100)
    _music8.play()

def stop_music():
    global _music1, _music2, _music3
    if _music1:
        _music1.stop()
    if _music2:
        _music2.stop()
    if _music3:
        _music3.stop()
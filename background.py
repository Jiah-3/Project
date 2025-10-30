from pico2d import load_image
import game_world

class Bg():
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)

    def set_bg(self, stage):
        if stage == 1:
            self.image = load_image('background.png')


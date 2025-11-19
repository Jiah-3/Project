from pico2d import load_image, load_font

import character


class Inventory:
    def __init__(self):
        self.char = character.Char()
        self.image = load_image('inventory.png')
        self.font = load_font('ENCR10B.TTF', 20)

    def draw(self):
        self.image.draw(400, 300)
        self.font.draw(30, 500, f'HP:{self.char.stat_hp}', (102, 255, 102))
        self.font.draw(30, 480, f'ATK:{self.char.stat_attack}', (255, 102, 102))
        self.font.draw(30, 460, f'DEF:{self.char.stat_defense}', (51, 153, 255))
        self.font.draw(30, 440, f'AGI:{self.char.stat_agility}', (255, 255, 255))
        self.font.draw(30, 420, f'LUK:{self.char.stat_luck}', (255, 255, 102))
        self.font.draw(30, 400, f'Stat_point:{self.char.stat_points}', (0, 0, 0))
        self.font.draw(30, 380, f'Gold:{self.char.gold}', (255, 200, 0))

    def update(self):
        pass
from pico2d import load_image, load_font

import character


class Inventory:
    def __init__(self):
        self.char = character.Char()
        self.image = load_image('inventory.png')
        self.font = load_font('ENCR10B.TTF', 20)

    def draw(self):
        self.image.draw(400, 300)

        self.char.image.clip_draw(100, 0, 100, 100, 400, 400)
        self.font.draw(30, 500, f'HP:{self.char.stat_hp}', (102, 255, 102))
        self.font.draw(30, 450, f'ATK:{self.char.stat_attack}', (255, 102, 102))
        self.font.draw(30, 400, f'DEF:{self.char.stat_defense}', (51, 153, 255))
        self.font.draw(30, 350, f'AGI:{self.char.stat_agility}', (255, 255, 255))
        self.font.draw(30, 300, f'LUK:{self.char.stat_luck}', (255, 255, 102))
        self.font.draw(30, 200, f'SP:{self.char.stat_points}', (0, 0, 0))
        self.font.draw(30, 150, f'Gold:{self.char.gold}', (255, 200, 0))

        self.font.draw(580, 500, f'Health:{self.char.hp}/{self.char.max_hp}', (102, 255, 102))
        self.font.draw(580, 480, f'Damage:{self.char.damage}', (255, 70, 70))
        self.font.draw(580, 460, f'Attack:{self.char.attack}%', (255, 70, 70))
        self.font.draw(580, 440, f'Defense:{self.char.defense}%', (51, 153, 255))
        self.font.draw(580, 420, f'Speed:{self.char.speed}%', (255, 255, 255))
        self.font.draw(580, 400, f'Dodge:{self.char.dodge}%', (255, 255, 255))
        self.font.draw(580, 380, f'Crit Chance:{self.char.crit_chance}', (255, 255, 102))


    def update(self):
        pass
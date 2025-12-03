from pico2d import load_image, load_font

import character
import character_state


class Inventory:
    def __init__(self):
        self.char = character.Char()
        if character_state.char != None:
            self.char = character_state.char
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

        self.font.draw(560, 500, f'Health:{self.char.hp:.1f}/{self.char.max_hp:.1f}', (102, 255, 102))
        self.font.draw(560, 480, f'Damage:{self.char.damage:.2f}', (255, 70, 70))
        self.font.draw(560, 460, f'Attack:{self.char.attack:.1f}%', (255, 70, 70))
        self.font.draw(560, 440, f'Defense:{self.char.defense:.1f}%', (51, 153, 255))
        self.font.draw(560, 420, f'Speed:{self.char.speed:.1f}%', (255, 255, 255))
        self.font.draw(560, 400, f'Dodge:{self.char.dodge:.1f}%', (255, 255, 255))
        self.font.draw(560, 380, f'Crit Chance:{self.char.crit_chance}', (255, 255, 102))

        for i in range(0, 9):
            if self.char.item[i] is not None:
                image = load_image(self.char.item[i][8])
                image.draw(310, 230)

    def update(self):
        pass
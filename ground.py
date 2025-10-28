from pico2d import load_image

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        self.x, self.y = 0, 0
        self.width = 50

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


def stage1_1():
    # 여러 Ground 생성 후 리스트로 반환
    positions = [(0, 30), (100, 30), (200, 30), (300, 30), (400, 30), (500, 30), (600, 30), (700, 30), (800, 30)]
    grounds = [Ground() for _ in positions]
    for ground, (x, y) in zip(grounds, positions):
        ground.x = x
        ground.y = y
    return grounds
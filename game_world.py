# world[0] : 가장 낮은 계층
# world[1] : 그 위의 계층
world = [[], [], []]

def add_object(o, depth=0):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    else:
        print("Object not in world")

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()
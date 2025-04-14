from time import sleep as wait

class GusinaBase(object):
    def __init__(self, name='Gusina Base'):
        self.name = name
        print "[" + name + "] initialization engine..."
        self.scene = Scene()
        global scene
        scene = self.scene

    def run(self):
        wait(2)
        print "[" + self.name + "] Launching the scene..."
        wait(1)
        for ent in scene.entities:
            print "Rendering: ", ent
        print "[" + self.name + "] The cycle is completed (deaf)"


class color:
    red = (1, 0, 0)
    white = (1, 1, 1)
    black = (0, 0, 0)

class Scene:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)

class Entity:
    def __init__(self, form='cube', color=color.white, pos=(0, 0, 0)):
        self.form = form
        self.color = color
        self.pos = pos
        scene.add(self)

    def __str__(self):
        return "Entity(form=%s, pos=%s)" % (self.form, self.pos)
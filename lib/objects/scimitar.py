import pygame
from . import set_hitbox

class   Scimitar:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.dimensions = dimensions
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/'  + 'scimitar_object.png'), (cls.dimensions, cls.dimensions))
        cls.img_recall = []
        for i in range(1, 5):
            cls.img_recall.append(pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/'  + 'scimitar_object_' + str(i) + '.png'), (cls.dimensions, cls.dimensions)))
        cls.env = env
        return cls

    def __init__(self, x, y, weapon):
        self.x = x
        self.y = y
        self.weapon = weapon
        self.ultimatum = 144
        self.recall = 0
        self.interval = 6

    def display(self, env):
        if self.ultimatum:
            env.mod.tools.display(env, self.img, self.x, self.y)
        elif not self.recall // self.interval > 3:
            env.mod.tools.display(env, self.img_recall[self.recall // self.interval], self.x, self.y)

    def update(self):
        if self.ultimatum:
            self.ultimatum -= 1
        else:
            self.recall += 1
            if self.recall // self.interval > 3:
                self.weapon.recall(self.x, self.y)
                self.disappear = True

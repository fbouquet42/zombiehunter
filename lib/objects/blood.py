import pygame

class   Blood:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'bullets/' + 'blood.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        env.mod.tools.display(env, self.img, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 24:
            self.disappear = True


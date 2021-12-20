import pygame

class   VampireMetamorphosis:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'vampire_metamorphosis.png'), (dimensions, dimensions))
        cls.img_dissipated = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'vampire_metamorphosis_dissipated.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        if self.time < 6:
            env.mod.tools.display(env, self.img, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img_dissipated, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 12:
            self.disappear = True


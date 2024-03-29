import pygame

class   DismountEffect:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'dismount_effect.png'), (dimensions, dimensions))
        cls.img_fades = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'dismount_effect_fades.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        if self.time > 9:
            env.mod.tools.display(env, self.img_fades, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 21:
            self.disappear = True


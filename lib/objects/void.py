import pygame

class   Void:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img_sucks = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'void_sucks.png'), (dimensions, dimensions))
        cls.img_expired = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'void_expired.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y, expired):
        self.x = x
        self.y = y
        self.expired = expired
        self.time = 0

    def display(self, env):
        if self.expired:
            env.mod.tools.display(env, self.img_expired, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img_sucks, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 7:
            self.disappear = True

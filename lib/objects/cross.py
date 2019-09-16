import pygame

class   Cross:
    disappear = False

    @classmethod
    def build_class(cls, env, name):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + name + '.png'), (env.player_dimensions, env.player_dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        if (self.time // 12) % 2:
            env.mod.tools.display(env, self.img, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 100:
            self.disappear = True


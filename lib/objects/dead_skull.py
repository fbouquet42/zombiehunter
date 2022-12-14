import pygame

class   DeadSkull:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img_1 = pygame.transform.scale(pygame.image.load(env.img_folder + 'bullets/' + 'lighting_skull_dead_1.png'), (dimensions, dimensions))
        cls.img_2 = pygame.transform.scale(pygame.image.load(env.img_folder + 'bullets/' + 'lighting_skull_dead_2.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 1
        self.frame = True

    def display(self, env):
        if self.frame:
            env.mod.tools.display(env, self.img_1, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img_2, self.x, self.y)

    def update(self):
        self.time += 1
        if not (self.time % 4):
            self.frame = not self.frame
        if self.time > 23:
            self.disappear = True


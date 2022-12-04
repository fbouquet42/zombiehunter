import pygame

class   FrogifiedLarge:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.fitting = dimensions // 2 
        dimensions *= 2
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'monsters/' + 'frogified.png'), (dimensions, dimensions))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        env.mod.tools.display(env, self.img, self.x - self.fitting, self.y - self.fitting)

    def update(self):
        self.time += 1
        if self.time > 8:
            self.disappear = True


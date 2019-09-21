import pygame

class   Fog:
    disappear = False
    time_fog = 45

    @classmethod
    def build_class(cls, env):
        cls.img_vial = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/'  + 'fog_vial_object.png'), (env.player_dimensions, env.player_dimensions))
        cls.img_fog = pygame.transform.scale(pygame.image.load(env.img_folder + 'bullets/' + 'fog.png'), (int(env.player_dimensions * 1.7), int(env.player_dimensions * 1.7)))
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        if self.time < self.time_fog:
            env.mod.tools.display(env, self.img_vial, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img_fog, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 499:
            self.disappear = True


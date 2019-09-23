import pygame
from threading import Thread
from random import randint

class   SummoningVial:
    disappear = False

    @classmethod
    def build_class(cls, env, zombie):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/'  + 'summoning_vial_object.png'), (env.player_dimensions, env.player_dimensions))
        cls.img_cloud = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/'  + 'summoning_cloud_object.png'), (env.player_dimensions, env.player_dimensions))
        cls.dimensions = env.player_dimensions
        cls.env = env
        cls.zombie = zombie
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0

    def display(self, env):
        if self.time >= 32:
            env.mod.tools.display(env, self.img_cloud, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time == 32:
            rand = randint(3, 4)
            for _ in range(0, rand):
                obj = self.zombie(self.env, self.x, self.y, randint(0, 8))
                t = Thread(target=obj.move, args=())
                t.daemon = True
                self.env.monsters.append(obj)
                t.start()
        if self.time > 36:
            self.disappear = True


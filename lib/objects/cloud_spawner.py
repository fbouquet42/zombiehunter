from random import randint
from . import Cloud

import pygame

class   CloudSpawner:
    disappear = False

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img_large = pygame.transform.scale(pygame.image.load(env.img_folder + 'foreground_cloud.png'), (env.width, env.height))
        cls.img_little = pygame.transform.scale(pygame.image.load(env.img_folder + 'foreground_little_cloud.png'), (env.width, env.height))
        return cls

    def __init__(self, monster):
        self.monster = monster
        self.time = 1

    def next_cloud(self):
        self.time = randint(1100, 3300)

    def spawn_cloud(self):
        cloud = Cloud(self.img_large if not randint(0, 4) else self.img_little, self.env.width, self.env.height)
        self.env.objects.append(cloud)

    def display(self, env):
        return

    def update(self):
        self.time -= 1
        if not self.time:
            self.spawn_cloud()
            self.next_cloud()
        if not self.monster.splited_lives:
            self.disappear = True


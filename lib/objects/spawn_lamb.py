import pygame
from random import randint
from threading import Thread

class   SpawnLamb:
    disappear = False

    @classmethod
    def build_class(cls, env, lamb):
        cls.env = env
        dimensions = env.player_dimensions
        cls.dimensions = dimensions
        cls.img_arrival = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'lamb_arrival.png'), (dimensions, dimensions))
        cls.img_spawn = pygame.transform.scale(pygame.image.load(env.img_folder + 'objects/' + 'lamb_spawn.png'), (dimensions, dimensions))
        cls.lamb = lamb
        return cls

    @classmethod
    def set_weapon(cls, weapon):
        cls.weapon = weapon

    def __init__(self, gargamel):
        self.gargamel = gargamel
        self.x = randint(0, self.env.width - self.dimensions)
        self.y = randint(0, self.env.height - self.dimensions)
        self.time = 0
        self.spawned = False

    def display(self, env):
        if self.spawned:
            env.mod.tools.display(env, self.img_spawn, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img_arrival, self.x, self.y)

    def update(self):
        if not self.gargamel.lives:
            self.disappear = True
            return
        self.time += 1
        if self.time > 29:
            if self.spawned:
                self.disappear = True
            else:
                monster = self.lamb(self.x, self.y)
                t = Thread(target=monster.move, args=())
                t.daemon = True
                self.env.monsters.append(monster)
                t.start()
                self.spawned = True
                self.time = 16
                self.weapon.spawned = 16

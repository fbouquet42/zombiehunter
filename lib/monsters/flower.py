
#Python Lib
import pygame
from random import randint
from threading import Thread

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster
from . import FlowerBush


class Flower(DefaultMonster):
    lives = 10
    name = "flower"
#    id_nb = 9
    degeneration = 200
    lifetime = 130
    rooted = True
    forest = True
    hunt = False
    attack = 0

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_bloom = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_bloom', cls.dimensions)

        cls.bush = FlowerBush.build_class(env, cls.img_dead)

        #built in carnivorous.py
        cls.gas = cls.env.mod.bullets.PoisonedGas
        cls.large_gas = cls.env.mod.bullets.PoisonedGasLarge
        return cls

    def __init__(self, target):
        self.x = target.x
        self.y = target.y
        self.direction = target.direction
        self.hitbox = set_hitbox_monster(self.env, self)
        self.bloom = 0

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
        return None, None

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.bloom:
            img = self.img_bloom[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()


    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if self._quit():
                return

        while self.degeneration:
            if self._quit():
                return

    def spawn_gas(self):
        if not randint(0, 4):
            gas = self.large_gas(self.x, self.y, randint(0, 7), self)
        else:
            gas = self.gas(self.x, self.y, randint(0, 7), self)
        t = Thread(target=gas.move, args=())
        t.daemon = True
        self.env.bullets.append(gas)
        t.start()

    def spawn_bush(self):
        bush = self.bush(self)
        t = Thread(target=bush.move, args=())
        t.daemon = True
        self.env.monsters.append(bush)
        t.start()
        self.lives = 0
        self.degeneration = 0

    def update(self):
        super().update()
        if not self.lives:
            return
        if self.lifetime:
            self.lifetime -= 1
            if not self.lifetime:
                if randint(0, 2):
                    self.bloom = 10
                else:
                    self.spawn_bush()
        if self.bloom:
            self.bloom -= 1
            if ((self.bloom + 1) % 2):
                self.spawn_gas()
            if not self.bloom:
                self.lives = 0

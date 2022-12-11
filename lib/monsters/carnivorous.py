
#Python Lib
import time
from random import randint
from threading import Thread

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class   Carnivorous(DefaultMonster):
    lives = 70
    name = "carnivorous"
    id_nb = 1
    attack = 2
    degeneration = 400
    rapidity = 0
    forest = True

    @classmethod
    def build_class(cls):
        cls.sniff = int(cls.dimensions * 1.5)
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_spelling = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_spelling', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.gas = cls.env.mod.bullets.PoisonedGas.build_class(cls.env)
        cls.large_gas = cls.env.mod.bullets.PoisonedGasLarge.build_class(cls.env)
        return cls

    def next_gas(self):
        self.will_gas = randint(75, 110)

    def spawn_gas(self):
        if not randint(0, 4):
            gas = self.large_gas(self.x, self.y, self.direction, self)
        else:
            gas = self.gas(self.x, self.y, self.direction, self)
        t = Thread(target=gas.move, args=())
        t.daemon = True
        self.env.bullets.append(gas)
        t.start()

    def __init__(self, direction, x, y):
        self.x = x
        self.y = y
        self.direction = direction
        self.target = self.env.players[0]
        self.hitbox = set_hitbox_monster(self.env, self, 0.46)

        self.spelling = 0
        self.next_gas()

    def _turn(self):
        if not self.stoned:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._turn()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.spelling:
            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed_large[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        if self.spelling:
            self.spelling -= 1
        super().update()
        if self.lives:
            self.will_gas -= 1
            if not self.will_gas:
                self.spawn_gas()
                self.spelling = 12
                self.next_gas()

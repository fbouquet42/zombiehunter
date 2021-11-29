
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Enyo(DefaultMonster):
    lives = 80
    name = "enyo"
    id_nb = 19
    attack = 2
    degeneration = 500

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        return cls


    def __init__(self, big_boss, x, y):
        self.direction = randint(0, 7)
        self.x = x
        self.y = y
        self.target = self.env.players[0]
        self.direction_blocked = 6

        self.hitbox = set_hitbox_monster(self.env, self, 0.46)
        self.rapidity = 11

        self.big_boss = big_boss

    def _action(self):
        if not self.stoned:
            if self.direction_blocked:
                direction = self.direction
            else:
                direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self._quit():
                return

        self.big_boss.splited_lives -= 1

        while self.degeneration:
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
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
        if self.direction_blocked:
            self.direction_blocked -= 1
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        self._perform_fire()
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5


#Python Lib
import time
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class   Cyclops(DefaultMonster):
    lives = 70
    eyeless = 30
    name = "cyclops"
    turn = 30
    hunt = True
    id_nb = 1
    attack = 2
    degeneration = 500

    @classmethod
    def build_class(cls):
        cls.sniff = int(cls.dimensions * 1.5)
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_night', cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_injured_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured_night', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_eyeless = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_eyeless', cls.dimensions)
        cls.img_eyeless_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_eyeless_night', cls.dimensions)
        cls.img_eyeless_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_eyeless_injured', cls.dimensions)
        cls.img_eyeless_injured_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_eyeless_injured_night', cls.dimensions)
        return cls

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.46)

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.rapidity = randint(5, 9)

        self.random = randint(0, 12)
        self.wait = self.turn


    def _no_eye(self, direction, distance):
        if distance is None:
            return None
        self.hunt = distance < self.sniff
        if self.hunt:
            return direction
        elif not self.wait:
            self.random = randint(0, 12)
            self.wait = self.turn
        else:
            self.wait -= 1
        return self.random

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if not self.stoned:
                direction, distance = self._sniff_fresh_flesh()
                if self.lives <= self.eyeless:
                    direction = self._no_eye(direction, distance)

                if direction is not None and direction < 8:
                    self.direction = direction
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                    self.hitbox.update_coords(self)

                if self.lives <= self.eyeless:
                    self.tools.limits(self, self.limitx, self.limity)
            self._target_hitted()
            if self._quit():
                return

        self.hunt = True
        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def _display_day(self, env, fitting):
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.lives > self.eyeless and self.injured:
            img = self.img_injured[self.direction]
        elif self.lives > self.eyeless:
            img = self.img[self.direction]
        elif self.injured:
            img = self.img_eyeless_injured[self.direction]
        else:
            img = self.img_eyeless[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)

    def _display_night(self, env, fitting):
        if not self.lives:
            return
        elif self.lives > self.eyeless and self.injured:
            img = self.img_injured_night[self.direction]
        elif self.lives > self.eyeless:
            img = self.img_night[self.direction]
        elif self.injured:
            img = self.img_eyeless_injured_night[self.direction]
        else:
            img = self.img_eyeless_night[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if env.night:
            self._display_night(env, fitting)
        else:
            self._display_day(env, fitting)
        self._debug()


#Python Lib
from threading import Thread
from random import randint

#Current Module
from . import DefaultMonster
from . import Frog
from . import set_hitbox_monster


class Target(object):
    def __init__(self, env, dimensions):
        self.x = randint(0, env.width)
        self.y = randint(0, env.height)
        self.dimensions = dimensions
        self.half = dimensions // 2
        self.hitbox = set_hitbox_monster(env, self)


class Vampire(DefaultMonster):
    lives = 60
    name = "vampire"
    id_nb = 21
    _resize = 0.9

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_bat = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', 'bat', int(cls.dimensions * cls._resize))
        cls.img_bat_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', 'bat' + '_injured', int(cls.dimensions * cls._resize))
        cls.metamorphosis = cls.env.mod.objects.VampireMetamorphosis.build_class(cls.env, cls.dimensions)
        return cls


    def _fly(self):
        self.env.objects.append(self.metamorphosis(self.x, self.y))
        self.target = Target(self.env, self.dimensions)
        self.hitbox = self.bat_hitbox

    def _land(self):
        self.env.objects.append(self.metamorphosis(self.x, self.y))
        self.ultimatum = 100
        self.vampire_hitbox.update_coords(self)
        self.hitbox = self.vampire_hitbox

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.bat_hitbox = set_hitbox_monster(env, self, self._resize * 0.24)
        self.vampire_hitbox = set_hitbox_monster(env, self)

        self.hitbox = self.vampire_hitbox
        self.rapidity = randint(9, 17)
        self.rapidity = 14 if self.rapidity > 14 else self.rapidity

        self.ultimatum = 0
        self._fly()

    def _get_direction_to_target(self):
        x, y, _ = self.tools.process_distance(self.target, self)
        return self._determine_direction(x, y)

    def _action(self):
        if not self.stoned:
            if self.ultimatum:
                direction, _ = self._sniff_fresh_flesh()
                if direction is not None:
                    self.direction = direction
            else:
                direction = self._get_direction_to_target()
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
                if self.affected(self.target):
                    self._land()
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self._quit():
                return

        if not self.ultimatum:
            self._land()
        while self.degeneration:
            if self.env.walking_dead:
                super()._action()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.ultimatum:
            fitting = fitting - (self.dimensions - self._resize * self.dimensions) // 2
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.ultimatum:
            if self.injured:
                img = self.img_injured[self.direction]
            else:
                img = self.img[self.direction]
        else:
            if self.injured:
                img = self.img_bat_injured[self.direction]
            else:
                img = self.img_bat[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()
        if self.lives and not self.ultimatum:
            self.tools.display(self.env, self.target.hitbox.img, self.target.hitbox.x, self.target.hitbox.y)

    def update(self):
        super().update()
        if self.lives and self.ultimatum:
            self.ultimatum -= 1
            if not self.ultimatum:
                self._fly()

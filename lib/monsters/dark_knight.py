
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class DarkKnight(DefaultMonster):
    lives = 150
    without_helmet = 70
    name = "dark_knight"
    id_nb = 10
    attack = 2

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_halberd = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'halberd', cls.dimensions)
        cls.img_dark_halberd = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'dark_halberd', cls.dimensions)
        cls.img_dark_halberd_injured = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'dark_halberd_injured', cls.dimensions)
        cls.img_helmet = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'helmet', cls.dimensions)
        cls.img_helmet_injured = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'helmet_injured', cls.dimensions)
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(11, 14)
        self.rapidity = 10 if self.rapidity > 10 else self.rapidity

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        helmet = None

        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.lives < self.without_helmet:
            if self.injured:
                img = self.img_injured[self.direction]
                self.tools.display(self.env, self.img_dark_halberd_injured[self.direction], self.x, self.y, fitting)
            else:
                img = self.img[self.direction]
                self.tools.display(self.env, self.img_dark_halberd[self.direction], self.x, self.y, fitting)
        else:
            if self.injured:
                img = self.img[self.direction]
                helmet = self.img_helmet_injured[self.direction]
            else:
                img = self.img[self.direction]
                helmet = self.img_helmet[self.direction]
            self.tools.display(self.env, self.img_halberd[self.direction], self.x, self.y, fitting)
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if helmet is not None:
            self.tools.display(self.env, helmet, self.x, self.y, fitting)
        self._debug()

    def hitted(self, attack=1):
        if self.lives >= self.without_helmet and self.lives - attack < self.without_helmet:
            self.attack = 3
            self.rapidity += 4
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.id_nb, 1
        return None, None

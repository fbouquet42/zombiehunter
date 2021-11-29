
#Python Lib
import time
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class   Devourer(DefaultMonster):
    lives = 130
    name = "devourer"
    hunt = True
    id_nb = 18
    attack = 2
    degeneration = 500

    @classmethod
    def build_class(cls):
        #cls.sniff = int(cls.dimensions * 1.5)
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_starved = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_starved', cls.dimensions)
        return cls

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.46)

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.rapidity = randint(7, 9)
        self.starved = False

        self.cooldown = randint(185, 310)


    def _stay_calm(self):
        calm = randint(55, 135)
        if self.cooldown < calm:
            self.cooldown = calm

    def _walk(self):
        self._stay_calm()
        self.rapidity = randint(4, 6)
        self.starved = False

    def _run(self):
        self.rapidity = randint(14, 16)
        self.starved = True

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            if self.starved:
                self._walk()
            else:
                self._stay_calm()
            self.injured = 12
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        elif self.starved:
            img = self.img_starved[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed_large[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        super().update()
        if self.cooldown and not self.starved:
            self.cooldown -= 1
            if not self.cooldown:
                self._run()

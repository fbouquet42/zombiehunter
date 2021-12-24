
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class Lamb(DefaultMonster):
    lives = 20
    name = "lamb"
    id_nb = 22
    attack = 1
    degeneration = 1

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.dead = cls.env.mod.objects.DeadLamb.build_class(cls.env, cls.dimensions)
        return cls


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target = self.env.players[0]

        self.hitbox = set_hitbox_monster(self.env, self)
        self.rapidity = randint(6, 9)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self._quit():
                return

        self.degeneration = 0
        self.env.objects.append(self.dead(self))

    def display(self, env):
        if not self.lives:
            return
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()

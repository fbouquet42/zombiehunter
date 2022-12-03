from random import randint

from . import DefaultMonster
from . import set_hitbox_monster

class   Vermine(DefaultMonster):
    name = "vermine"
    lives = 10
    id_nb = 23
    degeneration = 110
    target = None
    hunt = False
    turn = 18

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        return cls

    def __init__(self, father):
        self.x = father.x
        self.y = father.y
        self.hitbox = set_hitbox_monster(self.env, self, 0.24 * 0.9)

        self.rapidity = randint(10, 16)
        self.wait = self.turn

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting) #maybe have to rework this
        self._debug()

    def _fuss(self):
        if not self.wait:
            self.direction = randint(0, 7)
            self.wait = self.turn
        else:
            self.wait -= 1

    def _action(self):
        if not self.stoned:
            self._fuss()
            self.tools.move(self, self.direction, self.rapidity + self.env.furious)
            self.hitbox.update_coords(self)
        self._target_hitted()

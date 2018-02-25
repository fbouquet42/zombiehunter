from . import DefaultMonster
from . import set_hitbox_monster

from random import randint

class   Minion(DefaultMonster):
    name = "minion"
    lives = 30
    value = 2
    attack = 2
    id_nb = 4

    def build_class():
        Minion.img = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name, Minion.dimensions)
        Minion.img_injured = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name + '_injured', Minion.dimensions)
        Minion.img_dead = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name + '_dead', Minion.dimensions)
        return Minion

    def __init__(self, env, x, y):
        self.x = x
        self.y = y
        self.rapidity = randint(7, 13)
        self.rapidity = 11 if self.rapidity > 11 else self.rapidity
        self.hitbox = set_hitbox_monster(env, self, 0.26)
        self.target = env.players[0]

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

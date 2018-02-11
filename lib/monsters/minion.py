from . import DefaultMonster
from . import set_hitbox_monster

from random import randint

class   Minion(DefaultMonster):
    name = "minion"
    lives = 3
    value = 1

    def build_class():
        Minion.img = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name, Minion.dimensions)
        Minion.img_injured = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name + '_injured', Minion.dimensions)
        Minion.img_dead = Minion.tools.set_imgs(Minion.env.img_folder + 'monsters/', Minion.name + '_dead', Minion.dimensions)
        return Minion

    def __init__(self, env, x, y):
        self.x = x
        self.y = y
        self.rapidity = randint(3, 7)
        self.rapidity = 4 if self.rapidity > 4 else self.rapidity
        self.hitbox = set_hitbox_monster(env, self, 0.26)
        self.target = env.players[0]

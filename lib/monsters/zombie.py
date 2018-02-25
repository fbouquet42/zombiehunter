
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Zombie(DefaultMonster):
    lives = 20
    name = "zombie"
    id_nb = 0

    def build_class():
        Zombie.img = Zombie.tools.set_imgs(Zombie.env.img_folder + 'monsters/', Zombie.name, Zombie.dimensions)
        Zombie.img_injured = Zombie.tools.set_imgs(Zombie.env.img_folder + 'monsters/', Zombie.name + '_injured', Zombie.dimensions)
        Zombie.img_dead = Zombie.tools.set_imgs(Zombie.env.img_folder + 'monsters/', Zombie.name + '_dead', Zombie.dimensions)
        Zombie.img_possessed = Zombie.tools.set_imgs(Zombie.env.img_folder + 'monsters/', Zombie.name + '_possessed', Zombie.dimensions)
        return Zombie


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(5, 13)
        self.rapidity = 10 if self.rapidity > 10 else self.rapidity


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
        self._debug()

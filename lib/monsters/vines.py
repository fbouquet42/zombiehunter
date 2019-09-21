
#Python Lib
from random import randint
import time

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Vines(DefaultMonster):
    lives = 14
    name = "vines"
    forest = True
    rooted = True
    degeneration = 200
    rapidity = 0

    def build_class():
        Vines.img = Vines.tools.set_imgs(Vines.env.img_folder + 'monsters/', Vines.name, Vines.dimensions)
        Vines.img_dead = Vines.tools.set_imgs(Vines.env.img_folder + 'monsters/', Vines.name + '_dead', Vines.dimensions)
        return Vines


    def __init__(self, monster, target):
        target.fixed = True
        self.x = target.x
        self.y = target.y
        self.direction = target.direction
        self.target = target
        self.monster = monster

    def affected(self, bullet):
        return False

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if not self.monster.lives or not self.target.lives or self.target.shadow:
                break
            self.x = self.target.x
            self.y = self.target.y
            if self.target.direction != self.direction:
                self.direction = self.target.direction
                self.lives -= 1
            if self._quit():
                return
        self.target.fixed = False
        self.rooted = False
        self.lives = 0

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)

    def update(self):
        if not self.lives and self.degeneration:
            self.degeneration -= 1

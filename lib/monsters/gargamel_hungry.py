from threading import Thread
from random import randint
import time

from . import AbstractGargamel
from . import set_hitbox_monster

#2 phase, and sheep procession
class GargamelHungry(AbstractGargamel):
    lives = 880
    shield_lives = 60

    def __init__(self, env, x, y):
        self._random_spawn()
        self.target = self.env.players[0]

        self.set_weapons()

        self.weapon_left = pass
        self.weapon_right = pass

        #self.left_spell = pass
        #self.right_spell = pass

        self.left_types = []
        self.right_types = []

        self.hitbox = set_hitbox_monster(env, self, 0.25)
        
    def next_scimitar_spell(self):
        if self.have_scimitar:
            self.scimitar_spell = randint(43, 72)

    def next_spear_spell(self):
        if self.have_spear:
            self.spear_spell = randint(66, 102)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        direction = self.direction
        if not self.lives:
            img = self.img_dead[direction]
        elif self.injured:
            img = self.img_hungry_injured[direction]
        else:
            img = self.img_hungry[direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.have_scimitar:
            self.tools.display(self.env, self.img_scimitar[direction], self.x, self.y, fitting)
        if self.lives and self.have_spear:
            self.tools.display(self.env, self.img_spear[direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        super().update()

        if not self.lives:
            return
        if self.scimitar_spell:
            self.scimitar_spell -= 1
            if not self.scimitar_spell:
                self.have_scimitar = False
                self.env.objects.append(self.scimitar(self.x, self.y, self))
        else:
            self.next_scimitar_spell()
        if self.spear_spell:
            self.spear_spell -= 1
            if not self.spear_spell:
                self.have_spear = False
                self.env.objects.append(self.spear(self.x, self.y, self))
        else:
            self.next_spear_spell()

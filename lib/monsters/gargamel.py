from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster

class Gargamel(DefaultMonster):
    name = "gargamel"
    degeneration = 550
    lives = 200
    rapidity = 9
    attack = 3
    id_nb = 20

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.dimensions = int(self.dimensions * 3.25)
        self.half = self.dimensions // 2
        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
        self.img_weapon = self.tools.set_imgs(env.img_folder + 'weapons/', 'scimitar', self.dimensions)
        self.scimitar = env.mod.objects.Scimitar.build_class(env, self)
#        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)

        self.have_weapon = True
        self.spelling = False
        self.spell = 99
        #self.spell_type = [self.fire_spell , self.star_spell]

        self.hitbox = set_hitbox_monster(env, self, 0.25)

    def next_spell(self):
        if self.have_weapon:
            self.spell = randint(43, 72)

    def hitted(self, attack=1):
        if self.lives and not self.spelling:
            self.injured = 14
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                if not self.spelling:
                    self.tools.move(self, direction, self.rapidity)
                    self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        direction = self.direction
        if not self.lives:
            img = self.img_dead[direction]
        #elif self.spelling:
        #    img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[direction]
        else:
            img = self.img[direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.have_weapon:
            self.tools.display(self.env, self.img_weapon[direction], self.x, self.y, fitting)
        self._debug()


    def set_on_fire(self, n, player):
        pass

    def update(self):
        super().update()

        if self.spell:
            self.spell -= 1
            if not self.spell:
                self.have_weapon = False
                self.env.objects.append(self.scimitar(self.x, self.y))
        else:
            self.next_spell()

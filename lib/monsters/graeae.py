from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Deino
from . import Enyo
from . import Pemphredo

class Graeae(DefaultMonster):
    name = "graeae"
    degeneration = 150
    lives = 13
    rapidity = 7
    attack = 3
    id_nb = 19
    splited_lives = 3

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
#        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)

        self.blood = env.mod.objects.Blood.build_class(env, self.dimensions)
        self.spelling = False
        self.splited = [Deino.build_class(env), Enyo.build_class(env), Pemphredo.build_class(env)]
        #self.next_spell()
        #self.spell_type = [self.fire_spell , self.star_spell]

        self.hitbox = set_hitbox_monster(env, self, 0.7)

    def next_spell(self):
        self.spell = randint(430, 720)

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
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                    self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return
        self.env.objects.append(self.blood(self.x, self.y))
        for monster_type in self.splited:
            monster = monster_type(self, self.x, self.y)
            t = Thread(target=monster.move, args=())
            t.daemon = True
            self.env.monsters.insert(0, monster)
            t.start()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        #elif self.spelling:
        #    img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        self._debug()


    def _perform_fire(self):
        pass

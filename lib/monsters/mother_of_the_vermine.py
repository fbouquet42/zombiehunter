from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster

from .vermine import Vermine

class   MotherOfTheVermine(DefaultMonster):
    name = "mother_of_the_vermine"
    lives = 70
    id_nb = 21
    attack = 2
    degeneration = 500

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_singing = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_singing', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.vermine = cls.env.mod.monsters.Vermine.build_class()
        return cls

    def next_song(self):
        self.song = randint(115, 220)

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.48)

        self.rapidity = randint(5, 10)

        self.singing = 0
        self.next_song()

    def spawn_vermine(self):
        vermine = self.vermine(self)
        t = Thread(target=vermine.move, args=())
        t.daemon = True
        self.env.monsters.append(vermine)
        t.start()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        elif self.singing:
            img = self.img_singing[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            if self.singing:
                self.singing = 0
                self.next_song()
                self.song -= 22
            self.injured = 16
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.id_nb, 1
        return None, None

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if not self.stoned:
                direction, _ = self._sniff_fresh_flesh()
                if direction is not None:
                    self.direction = direction
                    if not self.singing:
                        self.tools.move(self, direction, self.rapidity + self.env.furious)
                        self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def update(self):
        super().update()
        if self.lives:
            if self.song:
                self.song -= 1
                if not self.song:
                    self.singing = 110
            elif self.singing:
                self.singing -= 1
                if not self.singing % 22:
                    self.spawn_vermine()
                if not self.singing:
                    self.next_song()


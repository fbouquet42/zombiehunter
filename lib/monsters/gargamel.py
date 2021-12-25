from threading import Thread
from random import randint
import time

from . import AbstractGargamel
from . import set_hitbox_monster
from . import Target

#2 phase, and sheep procession
class Gargamel(AbstractGargamel):
    lives = 880

    def __init__(self, env, x, y):
        self.set_weapons()
        self._random_spawn()
        self.target = self.env.players[0]

        self.weapon = self.scimitar(110)

        self.hitbox = set_hitbox_monster(env, self, 0.25)

        procession = self.procession(self.x, self.y, self)
        t = Thread(target=procession.spawn, args=())
        t.daemon = True
        self.env.bullets.append(procession)
        t.start()

        self.target_when_dead = Target(self.env, self.dimensions)
        self.target_when_dead.set_coords(self.x, self.y)

        self.env.background = self.env.background_butchery

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        direction = self.direction
        if not self.lives:
            img = self.img_hungry[direction]
        #elif self.scimitar_spelling:
        #    img = self.img_scimitar_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[direction]
        else:
            img = self.img[direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.weapon.in_hand:
            self.tools.display(self.env, self.weapon.img[direction], self.x, self.y, fitting)
        self._debug()

    def _get_direction_to_target(self):
        x, y, _ = self.tools.process_distance(self.target, self)
        return self._determine_direction(x, y)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                #if not self.spelling:
                self.tools.move(self, direction, self.rapidity)
                self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

        self.target = self.target_when_dead
        self.env.titles.append(self.title)
        while not self.affected(self.target):
            direction = self._get_direction_to_target()
            self.direction = direction
            self.tools.move(self, direction, self.rapidity + self.env.furious)
            self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

        self.env.titles.remove(self.title)
        self.env.background = self.env.background_basic
        self.degeneration = 0

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        self._perform_fire()
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if not self.lives:
            return
        self.weapon.update()
        if self.weapon.free:
            self.weapon = self.scimitar()

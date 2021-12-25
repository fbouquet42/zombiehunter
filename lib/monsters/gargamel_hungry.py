from threading import Thread
from random import randint
import time

from . import AbstractGargamel
from . import set_hitbox_monster
from . import Target

#2 phase, and sheep procession
class GargamelHungry(AbstractGargamel):
    lives = 70

    def __init__(self, env, x, y):
        self.set_dependencies()
        self._random_spawn()
        self.target = self.env.players[0]

        self.weapon_right = self.scimitar(110)
        self.weapon_left = self.nothing(self.weapon_right)

        self.right_weapons_types = [self.scimitar, self.shield]
        self.left_weapons_types = [self.spear]

        self.hitbox = set_hitbox_monster(env, self, 0.25)

        procession = self.procession(self.x, self.y, self, 405, 877)
        t = Thread(target=procession.spawn, args=())
        t.daemon = True
        self.env.bullets.append(procession)
        t.start()

        self.target_when_dead = Target(self.env, self.dimensions)
        self.target_when_dead.set_coords(self.x, self.y)

        self.env.background = self.env.background_butchery

        self.delay = 14

    def hitted(self, attack=1):
        if self.weapon_right.protect(attack):
            return self.id_nb, attack / 2
        if self.lives:
            self.injured = 14
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        direction = self.direction
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[direction]
            else:
                img = self.img_dead[direction]
        elif self.injured:
            img = self.img_hungry_injured[direction]
        else:
            img = self.img_hungry[direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.weapon_left.in_hand:
            self.tools.display(self.env, self.weapon_left.get_img()[direction], self.x, self.y, fitting)
        if self.lives and self.weapon_right.in_hand:
            self.tools.display(self.env, self.weapon_right.get_img()[direction], self.x, self.y, fitting)
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

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

        for lamb in self.env.lambs:
            lamb.lives = 0
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
            self.delay -= 1
            if not self.delay:
                if len(self.env.lambs):
                    self.env.lambs[0].lives = 0
                self.delay = 14
            return
        self.weapon_left.update()
        self.weapon_right.update()
        if self.weapon_left.free:
            self.weapon_left = self.left_weapons_types[randint(0, len(self.left_weapons_types) - 1)]()
        if self.weapon_right.free:
            self.weapon_right = self.right_weapons_types[randint(0, len(self.right_weapons_types) - 1)]()

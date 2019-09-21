from random import randint
from threading import Thread
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Ghost

class   Necromancer(DefaultMonster):
    lives = 60
    name = "necromancer"
    id_nb = 5

    def build_class():
        Necromancer.img = Necromancer.tools.set_imgs(Necromancer.env.img_folder + 'monsters/', Necromancer.name, Necromancer.dimensions)
        Necromancer.img_injured = Necromancer.tools.set_imgs(Necromancer.env.img_folder + 'monsters/', Necromancer.name + '_injured', Necromancer.dimensions)
        Necromancer.img_ghost = Necromancer.tools.set_imgs(Necromancer.env.img_folder + 'monsters/', Necromancer.name + '_ghost', Necromancer.dimensions)
        return Necromancer

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.rapidity = randint(7, 10)
        self.hitbox = set_hitbox_monster(env, self)

        self.out = True
        self.limitx = env.width - self.half
        self.limity = env.height - self.half
        self.spelling = 65
        self.ghost = Ghost

    def _center_reached(self):
        if self.x < -self.half or self.y < -self.half or self.y > self.limity or self.x > self.limitx:
            return False
        return True

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            if self.out:
                self.out = not self._center_reached()
            elif self.spelling:
                self.spelling -= 1
                if not self.spelling:
                    self.env.walking_dead += 1
            if self._quit():
                return

        if self.spelling:
            self.env.walking_dead += 1

        ghost = self.ghost(self.env, self.x, self.y, self.img_ghost)
        t = Thread(target=ghost.move, args=())
        t.daemon = True
        self.env.monsters.append(ghost)
        self.degeneration = 0
        t.start()
        
    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5

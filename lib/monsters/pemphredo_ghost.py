import time

from . import DefaultMonster
from . import set_hitbox_monster

class PemphredoGhost(DefaultMonster):
    lives = 1
    name = "pemphredo_ghost"
    rapidity = 16
    ultimatum = 450
    attack = 2
    rooted = True

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = set_hitbox_monster(self.env, self, 0.66)
        self.target = self.env.players[0]
        self.env.walking_dead += 1

    def affected(self, bullet):
        return False

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.ultimatum:
            self._action()
            self.ultimatum -= 1
            if self._quit():
                return
        self.degeneration = 0
        self.env.walking_dead -= 1

    def display(self, env):
        if not self.ultimatum:
            return
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.tools.display(env, self.img[self.direction], self.x, self.y, fitting)
        self._debug()

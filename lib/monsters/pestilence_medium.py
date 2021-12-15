import time

from . import DefaultMonster
from . import set_hitbox_monster

class PestilenceMedium(DefaultMonster):
    name = "pestilence_medium"
    ultimatum = 145
    lives = 1
    attack = 1
    hunt = False
    poison = 100

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        return cls

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.hitbox = set_hitbox_monster(self.env, self, 0.46)

    def affected(self, bullet):
        return False

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                if player.lives:
                    player.poisoned = self.poison

    def drip(self):
        self.tick = self.env.mod.tools.Tick()
        while self.ultimatum:
            self._target_hitted()
            self.ultimatum -= 1
            if self._quit():
                return
        self.degeneration = 0

    def display(self, env):
        if not self.ultimatum:
            return
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.tools.display(env, self.img[self.direction], self.x, self.y, fitting)
        self._debug()

    def _perform_fire(self):
        pass

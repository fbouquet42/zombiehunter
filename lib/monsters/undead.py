import time

from . import DefaultMonster
from . import set_hitbox_monster

class   Undead(DefaultMonster):
    lives = 0
    name = "zombie"

    def __init__(self, env, player):
        self.x = player.x
        self.y = player.y
        self.direction = player.direction
        self.player = player

        self.rapidity = 4
        self.img = player.img_possessed
        self.hitbox = set_hitbox_monster(env, self)
        self.target = env.players[0]

    def target_hitted(self):
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                player.hitted()

    def move(self):
        self.time = time.time()
        while self.env.walking_dead:
            self._action()
            self.player.x = self.x
            self.player.y = self.y
            if self._quit():
                return
        self.player.direction = self.direction
        self.player.possessed = False
        self.degeneration = 0

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        self.tools.display(env, self.img[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        pass

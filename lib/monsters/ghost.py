from . import DefaultMonster
from . import set_hitbox_monster

class Ghost(DefaultMonster):
    name = "ghost"
    rapidity = 6
    ultimatum = 280

    def __init__(self, env, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.hitbox = set_hitbox_monster(env, self, 0.26)
        self.target = self.env.players[0]

    def affected(self, bullet):
        return False

    def move(self):
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

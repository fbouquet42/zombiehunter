from random import randint

from . import set_hitbox_monster

class Target(object):
    def __init__(self, env, dimensions):
        self.dimensions = dimensions
        self.half = dimensions // 2
        self.x = randint(0, env.width - self.half)
        self.y = randint(0, env.height - self.half)
        self.hitbox = set_hitbox_monster(env, self)

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.update_coords(self)

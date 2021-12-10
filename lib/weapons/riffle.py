from threading import Thread
from random import randint

from . import AutomaticDefault

class   Riffle(AutomaticDefault):
    name = 'riffle'

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name, cls.dimensions)
        cls.bullet = env.mod.bullets.DoubleBullet.build_class(env)
        return cls

    def _loading(self):
        self.next_shoot = randint(140, 280)

    def __init__(self):
        self._loading()

    def update(self, monster):
        if self.next_shoot:
            self.next_shoot -= 1
        else:
            bullet = self.bullet(monster.x, monster.y, monster.direction, monster)
            t = Thread(target=bullet.move, args=())
            t.daemon = True
            self.env.bullets.append(bullet)
            t.start()
            self._loading()

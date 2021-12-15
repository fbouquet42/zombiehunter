from threading import Thread
from random import randint

from . import AutomaticDefault

class   TommyGun(AutomaticDefault):
    name = 'tommy_gun'

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name, cls.dimensions)
        cls.bullet = env.mod.bullets.Spore.build_class(env)
        return cls

    def _loading(self):
        if self.how_much:
            self.next_shoot = 6
            self.how_much -= 1
        else:
            self.next_shoot = randint(33, 77)
            self.how_much = randint(0, 2)

    def __init__(self):
        self.how_much = 0
        self._loading()

    def update(self, monster):
        if self.next_shoot:
            self.next_shoot -= 1
        else:
            bullet = self.bullet(monster.x, monster.y, monster.direction)
            t = Thread(target=bullet.move, args=())
            t.daemon = True
            self.env.bullets.append(bullet)
            t.start()
            self._loading()

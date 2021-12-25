#Python Lib
import time
from threading import Thread
from random import randint

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   LambsProcession(DefaultBullet):

    @classmethod
    def build_class(cls, lamb):
        cls.lamb = lamb
        return cls

    def _next_lamb(self):
        self.will_summon = randint(155, 255)
        self.number = randint(2, 5)

    def __init__(self, x, y, gargamel):
        super().__init__(x, y, 0)
        self.gargamel = gargamel
        self._next_lamb()

    def display(self, env):
        pass
    
    def spawn(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            if not self.will_summon:
                monster = self.lamb(self.x, self.y)
                t = Thread(target=monster.move, args=())
                t.daemon = True
                self.env.monsters.append(monster)
                t.start()
                if self.number:
                    self.will_summon = 8
                    self.number -= 1
                else:
                    self._next_lamb()
            if not self.gargamel.lives:
                return self._dead()
            self.will_summon -= 1
            if self._quit():
                return

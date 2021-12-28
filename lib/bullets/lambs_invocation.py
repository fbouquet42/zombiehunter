#Python Lib
import time
from threading import Thread
from random import randint

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   LambsInvocation(DefaultBullet):

    @classmethod
    def build_class(cls, lamb):
        cls.arrival = cls.env.mod.objects.SpawnLamb.build_class(cls.env, lamb)
        return cls

    def __init__(self, weapon, gargamel):
        self.alive = True
        self.weapon = weapon
        self.gargamel = gargamel
        self.ultimatum = 1

    def display(self, env):
        pass
    
    def spawn(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            if self.ultimatum:
                self.ultimatum -= 1
                if not self.ultimatum:
                    self.lamb = self.arrival(self.gargamel)
                    self.env.objects.append(self.lamb)
            elif self.lamb.spawned:
                self.ultimatum = 16
            if not self.gargamel.lives:
                return self._dead()
            if not self.weapon.in_hand:
                return self._dead()
            if self._quit():
                return

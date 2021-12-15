import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet
from random import randint

class   SmokeCloud(DefaultBullet):
    lifetime = 36
    attack = 0
    rapidity = 69
    name = "smoke_cloud"

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.img_set = [env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, player.dimensions), env.mod.tools.set_imgs(env.img_folder + "bullets/", "little_" + cls.name, player.dimensions), env.mod.tools.set_imgs(env.img_folder + "bullets/", "mini_" + cls.name, player.dimensions) ]
        cls.player = player
        cls.weapon = weapon
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction)
        self.img = self.img_set[randint(0, 2)]
        self.img_night = self.img

    def display(self, env):
        self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.lifetime -= 1
            if not self.lifetime:
                return self._dead()
            if self._quit():
                return

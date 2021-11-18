
#Python Lib
from threading import Thread
import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   FireBall(DefaultBullet):
    rapidity = 35
    attack = 10
    from_player=True
    name = "dragon_ball"

    @classmethod
    def pre_build(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.img_night = cls.img
        cls.player = player
        cls.weapon = weapon
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.15)
        self.tools.move(self, self.direction)

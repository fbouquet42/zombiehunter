#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Locust(DefaultBullet):
    rapidity = 23
    attack = 8

    @classmethod
    def build_class(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "locust", env.player_dimensions)
        return cls

    def __init__(self, x, y, direction, monster):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.19)
        self.monster = monster
        self.tools.move(self, self.direction)

    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        return ret

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   MagneticBullet(DefaultBullet):
    #rapidity = 24
    rapidity = 29
    name = "magnetic_bullet"
    attack=6

    @classmethod
    def build_class(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.tools.move(self, self.direction)
    
    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        return ret


#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Tooth(DefaultBullet):
    rapidity = 34
    attack=20
    from_player = True
    name = "tooth"

    @classmethod
    def pre_build(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "devil_tooth_tier2", env.player_dimensions)

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.img_night = cls.img
        cls.player = player
        cls.weapon = weapon
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction)

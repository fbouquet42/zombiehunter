#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Bullet(DefaultBullet):
    rapidity = 50
    from_player = True
    name = "bullet"

    @classmethod
    def build_class(cls, env, player):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, player.dimensions)
        cls.img_night = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + '_night', player.dimensions)
        cls.player = player
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction, 22)

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Bullet(DefaultBullet):
    rapidity = 29
    def build_class(env, player):
        Bullet.player = player
        Bullet.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "bullet", env.player_dimensions)
        return Bullet

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction, 22)

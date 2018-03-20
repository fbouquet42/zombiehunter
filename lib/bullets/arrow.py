#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Arrow(DefaultBullet):
    rapidity = 39
    attack=20
    from_player = True

    def build_class(env, player):
        Arrow.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "arrow", player.dimensions)
        Arrow.player = player
        return Arrow

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction)


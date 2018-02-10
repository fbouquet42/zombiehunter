#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Explosion(DefaultBullet):
    lifetime = 40
    def build_class(env, player):
        Explosion.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "explosion", player.dimensions)
        Explosion.player = player
        return Explosion

    def __init__(self, x, y, direction):
        super.__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.88)

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted()
        for monster in self.env.monsters:
            if not monster.injured and monster.affected(self):
                self.player.score += monster.hitted()

    def explose(self):
        while True:
            self.lifetime -= 1
            if not self.lifetime % 5:
                self.env.jerk = not self.env.jerk
            if not self.lifetime:
                self.env.jerk = False
                return self._dead()
            self._target_hitted()
            if self._quit():
                return


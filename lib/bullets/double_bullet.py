#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   DoubleBullet(DefaultBullet):
    rapidity = 23

    def build_class(env):
        DoubleBullet.img = env.mod.tools.set_imgs(env.img_src + "bullets/", "double_bullet", env.player_dimensions)
        return DoubleBullet

    def __init__(self, x, y, direction, monster):
        super.__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.monster = monster
        tools.move(self, self.direction)
    
    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted()
                ret = True
        for monster in self.env.monsters:
            if not monster is self.monster and monster.affected(self):
                monster.hitted()
                ret = True
        return ret


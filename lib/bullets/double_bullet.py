#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   DoubleBullet(DefaultBullet):
    rapidity = 43
    name = "double_bullet"

    @classmethod
    def build_class(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        cls.img_night = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + '_night', env.player_dimensions)
        return cls

    def __init__(self, x, y, direction, monster):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.monster = monster
        self.tools.move(self, self.direction)
    
    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        for monster in self.env.monsters:
            if not monster is self.monster and monster.affected(self):
                monster.hitted(attack=self.attack)
                ret = True
        return ret


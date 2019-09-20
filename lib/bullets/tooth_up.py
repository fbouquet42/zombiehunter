#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   ToothUp(DefaultBullet):
    rapidity = 48
    attack=20
    from_player = True
    name = "tooth_tier2"

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
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.tools.move(self, self.direction)

    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if not player.lives:
                continue
            if player is not self.player and player.affected(self):
                player.hitted(attack = self.attack // 2 if self.from_player else self.attack)
                ret = True
        for monster in self.env.monsters:
            if not monster.lives:
                continue
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value
                    self.weapon.xp += self.player.score.values[id_nb] * value
                ret = True
        return ret

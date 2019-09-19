#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   SonicBall(DefaultBullet):
    rapidity = 16
    attack=10
    from_player = True
    name = "sonic_ball"

    @classmethod
    def pre_build(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        cls.dimensions = env.player_dimensions

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.player = player
        cls.weapon = weapon
        cls.limitx = env.width
        cls.limity = env.height
        return cls

    def _limits_reached(self):
        if self.x < -self.dimensions or self.y < -self.dimensions or self.y > self.limity or self.x > self.limitx:
            return True
        return False

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.24)
        self.tools.move(self, self.direction)

    def _target_hitted(self):
        for monster in self.env.monsters:
            if not monster.lives:
                continue
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value
                    self.weapon.xp += self.player.score.values[id_nb] * value
        return False

import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   DevilExplosion(DefaultBullet):
    lifetime = 25
    attack = 2
    from_player = True
    name = "devil_explosion"

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
        self.hitbox = set_hitbox_bullet(self.env, self, 0.66)

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack // 2)
        for monster in self.env.monsters:
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value
                    self.weapon.xp += self.player.score.values[id_nb] * value

    def explose(self):
        self.tick = self.env.mod.tools.Tick()
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


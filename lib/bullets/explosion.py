import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Explosion(DefaultBullet):
    lifetime = 25
    attack = 2
    from_player = True
    name = "explosion"

    @classmethod
    def build_class(cls, env, player):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, player.dimensions)
        cls.img_night = cls.img
        cls.player = player
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.88)

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
        for monster in self.env.monsters:
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value

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


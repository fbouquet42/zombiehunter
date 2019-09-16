import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   DevilFire(DefaultBullet):
    lifetime = 15
    attack = 1
    from_player = True
    name = "devil_fire"

    @classmethod
    def build_class(cls, env, player):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, player.dimensions)
        cls.img_night = cls.img
        cls.player = player
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.36)

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
        for monster in self.env.monsters:
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value

    def burn(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.lifetime -= 1
            if not self.lifetime:
                return self._dead()
            self._target_hitted()
            if self._quit():
                return


import time

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Fear(DefaultBullet):
    lifetime = 8
    attack = 2
    name = "fear"

    @classmethod
    def build_class(cls):
        cls.img = cls.env.mod.tools.set_imgs(cls.env.img_folder + "bullets/", cls.name, cls.env.player_dimensions)
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
                monster.scares(12)

    def scares(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.lifetime -= 1
            if not self.lifetime:
                return self._dead()
            self._target_hitted()
            if self._quit():
                return


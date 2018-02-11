
#Python Lib
from threading import Thread
import time

#Current Module
from . import Explosion
from . import set_hitbox_bullet
from . import DefaultBullet

class   Rocket(DefaultBullet):
    rapidity = 20.
    def build_class(env, player):
        Rocket.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "rocket", player.dimensions)
        Rocket.player = player
        Rocket.explosion = Explosion.build_class(env, player)
        return Rocket

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.tools.move(self, self.direction)
        self.acceleration = 0.

    def _explose(self):
        explosion = self.explosion(self.x, self.y, self.direction)
        t = Thread(target=explosion.explose, args=())
        t.daemon = True
        self.env.bullets.append(explosion)
        t.start()

    def _target_hitted(self):
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                self._explose()
                return True
        for monster in self.env.monsters:
            if monster.affected(self):
                self._explose()
                return True
        return False

    def move(self):
        self.time = time.time()
        while True:
            self.tools.move(self, self.direction, int(self.rapidity + self.acceleration))
            if self.acceleration < 15.:
                self.acceleration += 0.4
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            if self._quit():
                return

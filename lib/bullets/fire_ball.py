
#Python Lib
from threading import Thread
import time

#Current Module
from . import DevilFire
from . import set_hitbox_bullet
from . import DefaultBullet

class   FireBall(DefaultBullet):
    rapidity = 35
    attack = 20
    from_player=True
    name = "devil_ball"

    @classmethod
    def pre_build(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        cls.img_night = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + '_night', env.player_dimensions)
        env.mod.bullets.DevilFire.pre_build(env)

    @classmethod
    def build_class(cls, env, player):
        cls.player = player
        cls.fire = DevilFire.build_class(env, player)
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.15)
        self.tools.move(self, self.direction)

    def _burn(self):
        fire = self.fire(self.x, self.y, self.direction)
        t = Thread(target=fire.burn, args=())
        t.daemon = True
        self.env.bullets.append(fire)
        t.start()

    def _target_hitted(self):
        for player in self.env.players:
            if player is not self.player and player.affected(self):
                player.hitted(attack=self.attack // 2)
                self._burn()
                return True
        for monster in self.env.monsters:
            if monster.affected(self):
                id_nb, value = monster.hitted(attack=self.attack)
                if id_nb is not None:
                    self.player.score.kills[id_nb] += value
                self._burn()
                return True
        return False

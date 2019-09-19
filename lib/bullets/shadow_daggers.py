from threading import Thread

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   ShadowDaggers(DefaultBullet):
    rapidity = 36
    attack=10
    from_player = True
    name = "shadow_daggers"

    @classmethod
    def pre_build(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions)
        cls.env = env

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.player = player
        cls.weapon = weapon
        return cls

    def __init__(self, x, y, direction, first=True):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        if first:
            obj = ShadowDaggers(self.x, self.y, self.direction, first=False)
            t = Thread(target=obj.move, args=())
            t.daemon = True
            self.env.bullets.append(obj)
            t.start()
        else:
            self.tools.move(self, self.direction)

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   DevilTooth(DefaultBullet):
    rapidity = 46
    attack=20
    from_player = True
    name = "devil_tooth"

    @classmethod
    def pre_build(cls, env):
        cls.imgs = [env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + '_left', env.player_dimensions), env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, env.player_dimensions), env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + '_right', env.player_dimensions) ]

    @classmethod
    def build_class(cls, env, player, weapon):
        cls.player = player
        cls.weapon = weapon
        return cls

    def __init__(self, x, y, direction, style):
        self.img = self.imgs[style]
        self.img_night = self.img
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self)
        self.tools.move(self, self.direction)
        self.style = style

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            if self.style == 1:
                self.tools.move(self, self.direction)
            elif self.style == 0:
                self.tools.move(self, self.direction, int(self.rapidity * 0.8))
                self.tools.move(self, (self.direction + 1) % 8, int(self.rapidity * 0.2), False)
            elif self.style == 2:
                self.tools.move(self, self.direction, int(self.rapidity * 0.8))
                self.tools.move(self, (self.direction + 7) % 8, int(self.rapidity * 0.2), False)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            if self._quit():
                return

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
                ret = True
        return ret

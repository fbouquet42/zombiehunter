#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   JellyFish(DefaultBullet):
    rapidity = 2
    rapidity_moving = 32
    moving = True
    attack = 8

    @classmethod
    def build_class(cls, env):
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", "jellyfish", env.player_dimensions)
        cls.img_moving = env.mod.tools.set_imgs(env.img_folder + "bullets/", "jellyfish_moving", env.player_dimensions)
        return cls

    def __init__(self, x, y, direction, monster):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.19)
        self.monster = monster
        self.tools.move(self, self.direction)
        self.ultimatum = 7

    def _change_state(self):
        if not self.moving:
            self.ultimatum = 7
        else:
            self.ultimatum = 13
        self.moving = not self.moving

    def display(self, env):
        if not self.moving:
            self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        else:
            self.tools.display(env, self.img_moving[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        return ret

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.tools.move(self, self.direction, self.rapidity if not self.moving else self.rapidity_moving)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            self.ultimatum -= 1
            if not self.ultimatum:
                self._change_state()
            if self._quit():
                return

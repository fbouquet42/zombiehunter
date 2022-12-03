#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   ThrowingKnife(DefaultBullet):
    rapidity = 33
    name = "knife"
    attack = 3

    @classmethod
    def build_class(cls, env, dimensions):
        cls.dimensions = dimensions
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, cls.dimensions)
        cls.limitx = env.width + cls.dimensions
        cls.limity = env.height + cls.dimensions
        return cls

    def __init__(self, x, y, direction, weapon):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.14)
        self.weapon = weapon
        self.tools.move(self, self.direction)
        self.ultimatum = 0

    def _limits_reached(self):
        if self.x < -self.dimensions or self.y < -self.dimensions or self.y > self.limity or self.x > self.limitx:
            return True
        return False

    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                self.weapon.recall(self.x, self.y)
                ret = True
        return ret

    def _dead(self):
        self.weapon.free = True
        self.alive = False

    def display(self, env):
        direction = (self.direction + (self.ultimatum % 16) // 2) % 8
        fitting = 0.23 * self.dimensions if direction % 2 else 0
        self.tools.display(env, self.img[direction], self.x, self.y, fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.tools.move(self, self.direction)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            self.ultimatum += 1
            if self._quit():
                return

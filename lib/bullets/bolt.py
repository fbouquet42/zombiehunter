from random import randint

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   Bolt(DefaultBullet):
    rapidity = 55
    name = "bolt"
    attack = 3

    @classmethod
    def build_class(cls, env):
        #cls.weapon_dimensions = weapon_dimensions
        cls.imgs = []
        cls.img = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name, cls.dimensions)
        #cls.dimensions_ratio = (weapon_dimensions - cls.dimensions) // 2
        cls.limitx = env.width + cls.dimensions
        cls.limity = env.height + cls.dimensions
        #cls.max_travel = int(env.height * 0.26)
        #cls.max_bump = int(env.height * 0.24) + cls.max_travel
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        #self.x += self.dimensions_ratio
        #self.y += self.dimensions_ratio
        self.hitbox = set_hitbox_bullet(self.env, self, 0.20)
        self.fitting = 0.23 * self.dimensions if direction % 2 else 0
        #self.ultimatum = 0
        #self.travelled_distance = 0
        self.tools.move(self, self.direction)

    def _limits_reached(self):
        if self.x < -self.dimensions or self.y < -self.dimensions or self.y > self.limity or self.x > self.limitx:
            return True
        return False

    def _target_hitted(self):
        ret = False
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                ret = True
        return ret
    
    def display(self, env):
        self.tools.display(env, self.img[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.tools.move(self, self.direction)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

from random import randint

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   LightingSkull(DefaultBullet):
    rapidity = 27
    name = "lighting_skull"
    attack = 33
    switch_img = 4

    @classmethod
    def build_class(cls, env):
        cls.dead_skull = env.mod.objects.DeadSkull.build_class(env, cls.dimensions)
        #cls.weapon_dimensions = weapon_dimensions
        cls.img_1 = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + "_1", cls.dimensions)
        cls.img_2 = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + "_2", cls.dimensions)
        #cls.dimensions_ratio = (weapon_dimensions - cls.dimensions) // 2
        cls.limitx = env.width + cls.dimensions
        cls.limity = env.height + cls.dimensions
        #cls.max_travel = int(env.height * 0.26)
        #cls.max_bump = int(env.height * 0.24) + cls.max_travel
        return cls

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.hitbox = set_hitbox_bullet(self.env, self, 0.20)
        self.fitting = 0.23 * self.dimensions if direction % 2 else 0
        self.tools.move(self, self.direction)
        self.frame = True
        self.time = self.switch_img

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
        self.time -= 1
        if not self.time:
            self.frame = not self.frame
            self.time = self.switch_img
        if self.frame:
            self.tools.display(env, self.img_1[self.direction], self.x, self.y, self.fitting)
        else:
            self.tools.display(env, self.img_2[self.direction], self.x, self.y, self.fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def _cursed_death(self):
        self.env.objects.append(self.dead_skull(self.x, self.y))
        self._dead()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self.tools.move(self, self.direction)
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._cursed_death()
            if self._quit():
                return

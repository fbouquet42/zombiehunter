from random import randint

#Current Module
from . import set_hitbox_bullet
from . import DefaultBullet

class   ThrowingLamb(DefaultBullet):
    rapidity = 25
    name = "lamb"
    attack = 3

    @classmethod
    def build_class(cls, env, weapon_dimensions):
        #cls.weapon_dimensions = weapon_dimensions
        cls.imgs = []
        cls.imgs.append(env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + "_projectile_1", cls.dimensions))
        cls.imgs.append(env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + "_projectile_2", cls.dimensions))
        cls.img_bumped = env.mod.tools.set_imgs(env.img_folder + "bullets/", cls.name + "_bumped", cls.dimensions)
        cls.dimensions_ratio = (weapon_dimensions - cls.dimensions) // 2
        cls.limitx = env.width + cls.dimensions
        cls.limity = env.height + cls.dimensions
        cls.max_travel = int(env.height * 0.26)
        cls.max_bump = int(env.height * 0.24) + cls.max_travel
        return cls

    def __init__(self, x, y, direction, weapon):
        super().__init__(x, y, direction)
        self.x += self.dimensions_ratio
        self.y += self.dimensions_ratio
        self.hitbox = set_hitbox_bullet(self.env, self, 0.20)
        self.weapon = weapon
        self.ultimatum = 0
        self.travelled_distance = 0
        self.down = False
        self.bumped = False
        self._internal_move()

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
    
    def _internal_move(self):
        self.travelled_distance += self.rapidity
        if not self.down:
            self.tools.move(self, self.direction)
        if not self.bumped and self.travelled_distance > self.max_travel:
            self.bumped = True
            self.rapidity = int(self.rapidity * 1.4)
        if not self.down and self.travelled_distance > self.max_bump:
            self.down = True

    def _dead(self):
        self.weapon.free = True
        self.alive = False

    def display(self, env):
        if self.bumped:
            direction = randint(0, 7)
            fitting = 0.23 * self.dimensions if direction % 2 else 0
            img = self.img_bumped[direction]
        else:
            fitting = self.fitting
            number = (self.ultimatum // 3) % len(self.imgs)
            img = self.imgs[number][self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if env.debug:
            self.tools.display(env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while True:
            self._internal_move()
            if self._limits_reached():
                return self._dead()
            self.hitbox.update_coords(self)
            if self._target_hitted():
                return self._dead()
            self.ultimatum += 1
            if self._quit():
                return


#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class   Cyclops(DefaultMonster):
    lives = 7
    eyeless = 3
    name = "cyclops"
    turn = 30
    hunt = True
    value = 3

    def build_class():
        Cyclops.sniff = int(Cyclops.dimensions * 1.5)
        Cyclops.img = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name, Cyclops.dimensions)
        Cyclops.img_injured = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name + '_injured', Cyclops.dimensions)
        Cyclops.img_eyeless = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name + '_eyeless', Cyclops.dimensions)
        Cyclops.img_eyeless_injured = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name + '_eyeless_injured', Cyclops.dimensions)
        Cyclops.img_dead = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name + '_dead', Cyclops.dimensions)
        Cyclops.img_possessed = Cyclops.tools.set_imgs(env.img_folder + 'monsters/', Cyclops.name + '_possessed', Cyclops.dimensions)
        return Cyclops

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.46)

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.rapidity = randint(2, 3)

        self.random = randint(0, 12)
        self.wait = self.turn


    def _no_eye(self, direction, distance):
        self.hunt = distance < self.sniff
        if self.hunt:
            return direction
        elif not self.wait:
            self.random = randint(0, 12)
            self.wait = self.turn
        else:
            self.wait -= 1
        return self.random

    def move(self):
        self.time = time.time()
        while self.lives:
            direction, distance = self._sniff_fresh_flesh()
            if self.lives <= self.eyeless:
                direction = self._no_eye(direction, distance)

            if direction is not None and direction < 8:
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)

            if self.lives <= self.eyeless:
                self.tools.limits(self, self.limitx, self.limity)
            self._target_hitted()
            if self._quit():
                return

        self.hunt = True
        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return


    def display(self):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.lives > self.eyeless and self.injured:
            img = self.img_injured[self.direction]
        elif self.lives > self.eyeless:
            img = self.img[self.direction]
        elif self.injured:
            img = self.img_eyeless_injured[self.direction]
        else:
            img = self.img_eyeless[self.direction]
        tools.display(self.env, img, self.x, self.y, fitting)
        self._debug()


#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class DarkKnight(DefaultMonster):
    lives = 160
    without_helmet = 90
    name = "dark_knight"
    id_nb = 12
    attack = 2

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_halberd = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'halberd', cls.dimensions)
        cls.img_dark_halberd = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'dark_halberd', cls.dimensions)
        cls.img_dark_halberd_injured = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'dark_halberd_injured', cls.dimensions)
        cls.img_helmet = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'helmet', cls.dimensions)
        cls.img_helmet_injured = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'helmet_injured', cls.dimensions)
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.28)

        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.rapidity = randint(11, 13)
        self.next_spell = 0
        self.spelling = 0
        self.charge = False

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        helmet = None

        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.lives < self.without_helmet:
            if self.injured:
                img = self.img_injured[self.direction]
                self.tools.display(self.env, self.img_dark_halberd_injured[self.direction], self.x, self.y, fitting)
            else:
                img = self.img[self.direction]
                self.tools.display(self.env, self.img_dark_halberd[self.direction], self.x, self.y, fitting)
        else:
            if self.injured:
                img = self.img[self.direction]
                helmet = self.img_helmet_injured[self.direction]
            else:
                img = self.img[self.direction]
                helmet = self.img_helmet[self.direction]
            self.tools.display(self.env, self.img_halberd[self.direction], self.x, self.y, fitting)
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if helmet is not None:
            self.tools.display(self.env, helmet, self.x, self.y, fitting)
        self._debug()

    def hitted(self, attack=1):
        if self.lives >= self.without_helmet and self.lives - attack < self.without_helmet:
            self.attack = 3
            self.next_spell = randint(65, 90)
            self.rapidity -= 1
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                self.spelling = 0
                if self.charge:
                    self.charge = False
                    self.rapidity -= 21
                return self.id_nb, 1
        return None, None

    def _action(self):
        if not self.stoned or self.lives >= self.without_helmet:
            if not self.charge:
                direction, _ = self._sniff_fresh_flesh()
            else:
                direction = self.direction
            if direction is not None:
                self.direction = direction
                if not self.spelling:
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def _limits_reached(self):
        if self.x < -self.half or self.y < -self.half or self.y > self.limity or self.x > self.limitx:
            return True
        return False

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if self.stoned and not self.env.stoned:
            self.stoned = False
        elif self.stoned:
            if self.charge:
                self.charge = False
                self.rapidity -= 21
                self.next_spell = randint(80, 100)
            elif self.spelling:
                self.spelling = 0
                self.next_spell = randint(40, 65)
            return

        if not self.lives:
            pass
        elif self.next_spell:
            self.next_spell -= 1
            if not self.next_spell:
                self.spelling = 32
        elif self.spelling:
            self.spelling -= 1
            if not self.spelling:
                self.charge = True
                self.rapidity += 21
        elif self.charge:
            if self._limits_reached():
                self.charge = False
                self.rapidity -= 21
                self.next_spell = randint(80, 100)

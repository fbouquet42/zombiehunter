
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Frog(DefaultMonster):
    lives = 20
    name = "frog"
    id_nb = 0
    direction_blocked = 0

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_jumping = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_jumping', cls.dimensions)
        cls.img_jumping_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_jumping_injured', cls.dimensions)
        cls.img_jumping_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_jumping_possessed', cls.dimensions)
        return cls

    def _next_jump(self):
        self.will_jump = randint(7, 9)

    def _shocked(self):
        self.will_jump = randint(14, 19)

    def __init__(self, direction, x, y):
        self.x = x
        self.y = y
        self.direction = direction
        self.target = self.env.players[0]
        self.hitbox = set_hitbox_monster(self.env, self)

        self.limitx = self.env.width - self.half
        self.limity = self.env.height - self.half

        self.rapidity = randint(13, 20)
        self.jumping = 0
        self._next_jump()

    def _action(self):
        if not self.stoned:
            if self.jumping and self.direction is not None:
                self.tools.move(self, self.direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
                self.tools.limits(self, self.limitx, self.limity)
            elif not self.jumping:
                direction, _ = self._sniff_fresh_flesh()
                if direction is not None:
                    self.direction = direction
        self._target_hitted()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                if self.jumping:
                    img = self.img_jumping_possessed[self.direction]
                else:
                    img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            if self.jumping:
                img = self.img_jumping_injured[self.direction]
            else:
                img = self.img_injured[self.direction]
        else:
            if self.jumping:
                img = self.img_jumping[self.direction]
            else:
                img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        self._perform_fire()
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if self.jumping:
            self.jumping -= 1
        elif self.lives:
            self.will_jump -= 1
            if not self.will_jump:
                if not randint(0, 9):
                    self.jumping = 7
                    self.direction = randint(0, 7)
                    self._shocked()
                else:
                    self.jumping = 4
                    self._next_jump()
        elif self.env.walking_dead:
            self.will_jump -= 1
            if not self.will_jump:
                self.jumping = 7
                broken_leg = randint(-1, 2)
                self.direction = (self.direction + 8 + broken_leg) % 8
                self._shocked()


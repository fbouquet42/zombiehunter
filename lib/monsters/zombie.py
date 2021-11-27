
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Zombie(DefaultMonster):
    lives = 20
    name = "zombie"
    id_nb = 0
    direction_blocked = 0

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_night', cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_injured_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured_night', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        return cls


    def __init__(self, env, x, y, direction_summoning=9):
        if direction_summoning == 9:
            self._father_init(x, y)
        else:
            self.x = x
            self.y = y
            self.target = self.env.players[0]
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(5, 13)
        self.rapidity = 10 if self.rapidity > 10 else self.rapidity

        if direction_summoning < 8:
            self.direction = direction_summoning
            self.direction_blocked = 6

    def _display_day(self, env, fitting):
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)

    def _display_night(self, env, fitting):
        if not self.lives:
            return
        elif self.injured:
            img = self.img_injured_night[self.direction]
        else:
            img = self.img_night[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if env.night:
            self._display_night(env, fitting)
        else:
            self._display_day(env, fitting)
        self._debug()

    def _action(self):
        if not self.stoned:
            if self.direction_blocked:
                direction = self.direction
            else:
                direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def update(self):
        if self.direction_blocked:
            self.direction_blocked -= 1
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.inflamed:
            self.inflamed -= 1
            if self.inflamed == 0:
                if randint(0, 5):
                    self.inflamed = 7
            if not self.inflamed % 7:
                self.lives -= 1
                self.injured += 3
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5

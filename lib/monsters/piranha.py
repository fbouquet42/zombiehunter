
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Piranha(DefaultMonster):
    lives = 50
    name = "piranha"
    id_nb = 10
    poison = 80
    injured_gradient = 28
    rooted = True
    degeneration = 350

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(9, 12)
        self.escape = [0, 0, 0]

    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                if self.lives:
                    player.poisoned = self.poison

    def _set_escape(self):
        self.escape[0] = (self.direction + 3) % 8
        self.escape[1] = (self.direction + 4) % 8
        self.escape[2] = (self.direction + 5) % 8

    def affected(self, bullet):
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            self._set_escape()
            return True
        return False

    def _action(self):
        if not self.stoned:
            if self.lives and self.injured:
                if not self.injured % 4:
                    direction = self.escape[randint(0, 2)]
                else:
                    direction = self.direction
            else:
                direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                self.tools.move(self, direction, self.rapidity + self.env.furious)
                self.hitbox.update_coords(self)
        self._target_hitted()

    def set_on_fire(self, n, player):
        pass

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
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
        self._debug()

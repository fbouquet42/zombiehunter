from threading import Thread
from random import randint

from . import DefaultMonster
from . import set_hitbox_monster

class   JackLantern(DefaultMonster):
    name = "jack_lantern"
    lives = 30
    id_nb = 2

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_night', cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_injured_night = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured_night', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.bullet  = cls.env.mod.bullets.DoubleBullet.build_class(cls.env)
        return cls

    def loading(self):
        self.next_shoot = randint(140, 280)

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(5, 8)

        self.loading()
        self.walking_dead = False

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

    def _display_night(self, env, fitting):
        if not self.lives:
            return
        elif self.injured:
            img = self.img_injured_night[self.direction]
        else:
            img = self.img_night[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if env.night:
            self._display_night(env, fitting)
        else:
            self._display_day(env, fitting)
        self._debug()

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.env.walking_dead and not self.walking_dead:
            self.loading()
            self.walking_dead = True
        elif not self.walking_dead:
            self.walking_dead = False
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
            self.loading()
        elif self.stoned:
            return

        if self.next_shoot:
            if self.lives or self.env.walking_dead:
                self.next_shoot -= 1
        elif self.lives or self.env.walking_dead:
            bullet = self.bullet(self.x, self.y, self.direction, self)
            t = Thread(target=bullet.move, args=())
            t.daemon = True
            self.env.bullets.append(bullet)
            t.start()
            self.loading()
        else:
            self.loading()

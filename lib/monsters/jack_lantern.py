from threading import Thread
from random import randint

from . import DefaultMonster
from . import set_hitbox_monster

class   JackLantern(DefaultMonster):
    name = "jack_lantern"
    lives = 30
    value = 3

    def build_class():
        JackLantern.img = JackLantern.tools.set_imgs(JackLantern.env.img_folder + 'monsters/', JackLantern.name, JackLantern.dimensions)
        JackLantern.img_injured = JackLantern.tools.set_imgs(JackLantern.env.img_folder + 'monsters/', JackLantern.name + '_injured', JackLantern.dimensions)
        JackLantern.img_dead = JackLantern.tools.set_imgs(JackLantern.env.img_folder + 'monsters/', JackLantern.name + '_dead', JackLantern.dimensions)
        JackLantern.img_possessed = JackLantern.tools.set_imgs(JackLantern.env.img_folder + 'monsters/', JackLantern.name + '_possessed', JackLantern.dimensions)
        JackLantern.bullet = JackLantern.env.mod.bullets.DoubleBullet.build_class(JackLantern.env)
        return JackLantern

    def loading(self):
        self.next_shoot = randint(180, 360)

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(2, 3)

        self.loading()
        self.walking_dead = False

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

    def update(self):
        if self.env.walking_dead and not self.walking_dead:
            self.loading()
            self.walking_dead = True
        elif not self.walking_dead:
            self.walking_dead = False
        if self.injured:
            self.injured -= 1
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
        if not self.lives and self.degeneration:
            self.degeneration -= 1


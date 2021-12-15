
#Python Lib
from threading import Thread
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster
from . import Garou

class Villager(DefaultMonster):
    lives = 10
    name = "villager"
    id_nb = 13
    degeneration = 350

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_transforming = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_transforming', cls.dimensions)
        cls.garou = Garou.build_class()
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.env = env
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(5, 9)

        self.out = True
        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.transforming = 0
        self.ultimatum = randint(114, 215)
        self.follow = True
        self.random = randint(0, 12)

    def _center_reached(self):
        if self.x < -self.half or self.y < -self.half or self.y > self.limity or self.x > self.limitx:
            return False
        return True

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if not self.stoned and not self.transforming:
                if not self.follow:
                    direction = self.random
                else:
                    direction, _ = self._sniff_fresh_flesh()

                if direction is not None and direction < 8:
                    self.direction = direction
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                    self.hitbox.update_coords(self)

                if self.out:
                    self.out = not self._center_reached()

                if not self.follow:
                    self.tools.limits(self, self.limitx, self.limity)

            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

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
        if not self.lives or self.out:
            pass
        elif self.ultimatum:
            self.ultimatum -= 1
            if not self.ultimatum:
                self.transforming = 105
            elif not self.ultimatum % 50:
                self.follow = not self.follow
                if self.follow:
                    self.random = randint(0, 12)
        elif self.transforming:
            self.transforming -= 1
            if not self.transforming:
                monster = self.garou(self.env, self.x, self.y)
                t = Thread(target=monster.move, args=())
                t.daemon = True
                self.env.monsters.append(monster)
                t.start()
                self.degeneration = 0
                self.lives = 0

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        elif self.transforming:
            img = self.img_transforming[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()

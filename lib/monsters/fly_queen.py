
#Python Lib
from threading import Thread
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

class FlyQueen(DefaultMonster):
    lives = 60
    name = "fly_queen"
    id_nb = 17
    degeneration = 350

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_spelling = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_spelling', cls.dimensions)
        cls.bullet = cls.env.mod.bullets.Locust.build_class(cls.env)
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.env = env
        self.hitbox = set_hitbox_monster(env, self, 0.26)

        self.rapidity = randint(5, 10)
        self.rapidity = 7 if self.rapidity < 7 else self.rapidity

        self.out = True
        self.limitx = env.width - self.half
        self.limity = env.height - self.half

        self.spelling = self.next_spell()
        self.heals = 0

    def next_spell(self):
        return randint(105, 165)

    def _center_reached(self):
        if self.x < -self.half or self.y < -self.half or self.y > self.limity or self.x > self.limitx:
            return False
        return True

    def update(self):
        if self.out:
            self.out = not self._center_reached()
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if not self.lives or self.out or self.stoned:
            pass
        else:
            self.spelling -= 1
            if not self.spelling:
                bullet = self.bullet(self.x, self.y, self.direction, self)
                t = Thread(target=bullet.move, args=())
                t.daemon = True
                self.env.bullets.append(bullet)
                t.start()
                self.spelling = self.next_spell()

            self.heals += 1
            if self.heals == 110:
                self.heals = 0
                for monster in self.env.monsters:
                    if monster.insect:
                        monster.is_healed()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        elif self.spelling < 30:
            img = self.img_spelling[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable[self.direction], self.x, self.y, fitting)
        self._debug()


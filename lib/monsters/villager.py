
#Python Lib
from threading import Thread
from random import randint

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster
from . import Garou
from . import Target

#IDEA: villager flew away and give a lot of points if they are still alive when hitted
class Villager(DefaultMonster):
    lives = 1
    name = "villager"
    id_nb = 13
    attack = 0

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_delivered = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_delivered', cls.dimensions)
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

        self.target_when_dead = Target(self.env, self.dimensions)
        self.target_when_dead.set_coords(self.x, self.y)

    def _center_reached(self):
        if self.x < -self.half or self.y < -self.half or self.y > self.limity or self.x > self.limitx:
            return False
        return True

    def _get_direction_to_target(self):
        x, y, _ = self.tools.process_distance(self.target, self)
        return self._determine_direction(x, y)

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

        if not self.degeneration:
            return

        self.target = self.target_when_dead
        self.env.objects.append(self.deliverance_effect(self.x, self.y))
        while not self.affected(self.target):
            direction = self._get_direction_to_target()
            self.direction = direction
            self.tools.move(self, direction, self.rapidity + self.env.furious)
            self.hitbox.update_coords(self)
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
            img = self.img_delivered[self.direction]
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

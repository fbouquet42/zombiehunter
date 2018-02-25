from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Minion
from . import FireBall

class Daemon(DefaultMonster):
    name = "daemon"
    lives = 1350
    fury_1 = 900
    fury_2 = 450
    rapidity = 7
    attack = 3
    id_nb = 3

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
        self.img_furious = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_furious', self.dimensions)
        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)
        self.img_shooting = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_shooting', self.dimensions)


        self.minion = Minion.build_class()
        self.fire_ball = FireBall.build_class()
        self.hell_star = env.mod.bullets.HellStar.build_class(env, self)

        self.furious = 0
        self.shooting = 0
        self.fire_star = 0
        self.summoning = 4

        self.spelling = False
        self.next_spell()
        self.spell_type = [self.fire_spell , self.star_spell]

        self.hitbox = set_hitbox_monster(env, self, 0.7)

    def fury_mod(self, time):
        self.furious = time
        self.env.furious = 2
        self.spelling = False
        self.spell += 25
        self.shooting = 0

    def next_spell(self):
        self.spell = randint(480, 840)

    def hitted(self, attack=1):
        if self.lives and not self.furious and not self.spelling:
            self.injured = 12
            if self.lives > self.fury_2 and self.lives - attack <= self.fury_2:
                self.fury_mod(888)
            elif self.lives > self.fury_1 and self.lives - attack <= self.fury_1:
                self.fury_mod(666)
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                if not self.spelling:
                    self.tools.move(self, direction, self.rapidity + self.env.furious)
                    self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        elif self.furious:
            img = self.img_furious[self.direction]
        elif self.spelling:
            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        if self.lives and self.shooting:
            shooting = self.shooting // 10
            self.tools.display(env, self.img_shooting[shooting % 8], self.x, self.y, 0.23 * self.dimensions if shooting % 2 else 0)
        self._debug()

    def get_coords(self, i):
        x = self.x
        y = self.y
        if i == 1:
            y = self.y + self.half
        elif i == 2:
            y = self.y - self.half
        elif i == 3:
            x = self.x - self.half
        elif i == 4:
            x = self.x + self.half
        return x, y

    def fire_spell(self):
        self.shooting = 1

    def star_spell(self):
        self.fire_star = 80
        if self.summoning:
            x, y = self.get_coords(self.summoning)
            hell_star = self.hell_star(x, y, self.direction)
            t = Thread(target=hell_star.move, args=())
            t.daemon = True
            self.env.bullets.append(hell_star)
            t.start()
            self.summoning -= 1

    def firing(self):
        self.shooting = 0
        for i in range(1, 5):
            x, y = self.get_coords(i)
            fire_ball = self.fire_ball(self.env, self, x, y, self.env.players[randint(0, len(self.env.players)) - 1])
            t = Thread(target=fire_ball.move, args=())
            t.daemon = True
            self.env.monsters.append(fire_ball)
            t.start()
        self.spelling = False

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1

        if not self.lives:
            pass
        elif self.furious:
            self.furious -= 1
            if not self.furious:
                self.env.furious = 0
        elif self.shooting > 120:
            self.firing()
        elif self.shooting:
            self.shooting += 1
        elif self.fire_star:
            self.fire_star -= 1
            if not self.fire_star:
                self.spelling = False
        elif self.spell:
            self.spell -= 1
        else:
            self.spell_type[randint(0, len(self.spell_type) - 1)]()
            self.next_spell()
            self.spelling = True

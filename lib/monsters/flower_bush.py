
#Python Lib
import pygame
from random import randint
from threading import Thread

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster

# croissance ?

class FlowerBush(DefaultMonster):
    lives = 10
    name = "flower_bush"
#    id_nb = 9
    degeneration = 200
    lifetime = 75
    rooted = True
    forest = True
    hunt = False
    attack = 2
    poison = 50

    @classmethod
    def build_class(cls, env, img_dead):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = img_dead
        return cls

    def __init__(self, flower):
        self.x = flower.x
        self.y = flower.y
        self.direction = flower.direction
        self.hitbox = set_hitbox_monster(self.env, self, 0.48)

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
        return None, None

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
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
        self._debug()


    def _target_hitted(self):
        for player in self.env.players:
            if player.affected(self):
                player.hitted(attack=self.attack)
                if self.lives:
                    player.poisoned = self.poison
                if self.inflamed and not randint(0, 3):
                    player.inflamed = 1
        if self.inflamed:
            for monster in self.env.monsters:
                if monster == self:
                    continue
                elif monster.affected(self) and not monster.inflamed:
                    if not randint(0, 3):
                        monster.set_on_fire(1, self.master_of_flames)

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._target_hitted()
            if self._quit():
                return

        while self.degeneration:
            if self._quit():
                return

    def update(self):
        super().update()
        if self.lifetime:
            self.lifetime -= 1
            if not self.lifetime:
                self.lives = 0
                """
                wall = Brambles(self, self.number - 1)
                t = Thread(target=wall.move, args=())
                t.daemon = True
                self.env.monsters.append(wall)
                t.start()
                """

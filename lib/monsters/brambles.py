
#Python Lib
import pygame
from random import randint
from threading import Thread

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Brambles(DefaultMonster):
    lives = 40
    name = "brambles"
#    id_nb = 9
    degeneration = 200
    lifetime = 330
    rooted = True
    forest = True

    @classmethod
    def build_class(cls, env):
        cls.env = env
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        return cls

    def __init__(self, monster, number, direction=None):
        self.monster = monster
        self.x = monster.x
        self.y = monster.y
        self.number = number
        self.hitbox = set_hitbox_monster(self.env, self)
        self.spawn_next = 4

        if direction is None:
            self.direction = monster.direction
            self.rapidity = int(self.hitbox.dimensions * 0.9)
            self._action()
        else:
            self.target = None
            self.direction = direction
            self.rapidity = int(self.monster.hitbox.dimensions * 1.2)
            self.tools.move(self, self.direction, self.rapidity)
            self.hitbox.update_coords(self)
            self._target_hitted()


    def _debug(self):
        if self.env.debug and self.lives:
            if self.target is not None and self.spawn_next:
                pygame.draw.line(self.env.GameWindow, (255, 0, 0), (self.target.x + self.target.half, self.target.y + self.target.half), (self.x + self.half, self.y + self.half))
            self.tools.display(self.env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

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
            self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed[self.direction], self.x, self.y, fitting)
        self._debug()


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
        if self.spawn_next:
            self.spawn_next -= 1
            if not self.spawn_next and self.number:
                wall = Brambles(self, self.number - 1)
                t = Thread(target=wall.move, args=())
                t.daemon = True
                self.env.monsters.append(wall)
                t.start()

import pygame
from random import randint

class   Cloud:
    disappear = False

    def __init__(self, img, width, height):
        self.img = img
        hh = height // 2
        h9 = int(height * 0.8)
        self.y = randint(-hh, h9)

        if not randint(0, 1):
            self.condition = width * 2
            self.x = - width
            self.move = self.move_r
        else:
            self.condition = - width
            self.x = width * 2
            self.move = self.move_l

    def display(self, env):
        env.mod.tools.display(env, self.img, self.x, self.y)

    def move_r(self):
        self.x += 1
        if self.x > self.condition:
            self.disappear = True

    def move_l(self):
        self.x -= 1
        if self.x < self.condition:
            self.disappear = True

    def update(self):
        self.move()


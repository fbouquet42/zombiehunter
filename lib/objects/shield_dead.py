import pygame

class   ShieldDead(object):
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img = env.mod.tools.set_imgs(env.img_folder + 'objects/', 'shield_dead', dimensions)
        return cls

    def __init__(self, monster):
        self.x = monster.x
        self.y = monster.y
        self.direction = monster.direction
        self.time = 0

    def display(self, env):
        env.mod.tools.display(env, self.img[self.direction], self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 16:
            self.disappear = True


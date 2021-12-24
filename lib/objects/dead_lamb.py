import pygame

class   DeadLamb:
    disappear = False

    @classmethod
    def build_class(cls, env, dimensions):
        cls.img = env.mod.tools.set_imgs(env.img_folder + 'objects/', 'lamb_dead', dimensions)
        return cls

    def __init__(self, lamb):
        self.x = lamb.x
        self.y = lamb.y
        self.direction = lamb.direction
        self.time = 0

    def display(self, env):
        env.mod.tools.display(env, self.img[self.direction], self.x, self.y)

    def update(self):
        self.time += 1
        if self.time > 16:
            self.disappear = True


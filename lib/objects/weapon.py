import pygame
from . import set_hitbox

class   Weapon:
    disappear = False

    def __init__(self, env, x, y, builder):
        self.env = env

        self.dimensions = env.player_dimensions
        self.x = x
        self.y = y

        self.hitbox = set_hitbox(env, self)

        self.builder = builder
        self.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/' + builder.name + '.png'), (env.player_dimensions, env.player_dimensions))
        self.time = 0

    def display(self, env):
        if self.disappear:
            return

        if self.time < 140:
            env.mod.tools.display(env, self.img, self.x, self.y)
        elif (self.time // 10) % 2:
            env.mod.tools.display(env, self.img, self.x, self.y)
        self._debug()

    def update(self):
        if self.disappear:
            return

        for player in self.env.players:
            if player.affected(self):
                self.disappear = True
                player.weapon.desequip()
                player.weapon = self.builder(self.env, player)
                return
        self.time += 1
        if self.time > 200:
            self.disappear = True

    def _debug(self):
        if self.env.debug and not self.disappear:
            self.env.mod.tools.display(self.env, self.hitbox.img, self.hitbox.x, self.hitbox.y)

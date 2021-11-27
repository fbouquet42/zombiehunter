import pygame
from . import set_hitbox

class   InvulnerableVial:
    disappear = False

    @classmethod
    def build_class(cls, env):
        cls.img = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/'  + 'invulnerable_vial_object.png'), (env.player_dimensions, env.player_dimensions))
        cls.img_cloud = pygame.transform.scale(pygame.image.load(env.img_folder + 'weapons/'  + 'invulnerable_cloud_object.png'), (env.player_dimensions, env.player_dimensions))
        cls.dimensions = env.player_dimensions
        cls.env = env
        return cls

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        self.hitbox = set_hitbox(self.env, self, 0.93)

    def display(self, env):
        if self.time >= 32:
            env.mod.tools.display(env, self.img_cloud, self.x, self.y)
        else:
            env.mod.tools.display(env, self.img, self.x, self.y)

    def update(self):
        self.time += 1
        if self.time == 32:
            for monster in self.env.monsters:
                if monster.affected(self) and monster.potion_effect:
                    monster.reset_bad_effect()
                    monster.invulnerable = 128
        if self.time > 36:
            self.disappear = True


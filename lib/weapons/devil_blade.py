from . import DefaultWeapon
from threading import Thread

class   DevilBlade(DefaultWeapon):
    name = 'devil_blade'

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name, cls.dimensions)
        cls.img_slash = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_slash', cls.dimensions)

        env.mod.bullets.DevilSlash.pre_build(env)
#        env.mod.bullets.DevilTooth.pre_build(env)

    def __init__(self, env, player):
        self.env = env
        self.player = player
        self.player.rage = True

        self.delay = 14
        self.cooldown = 0

        self.slash = env.mod.bullets.DevilSlash.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.cooldown <= (self.delay - 2):
            img = self.img[direction]
        else:
            img = self.img_slash[direction]
        self.tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        if self.cooldown:
            return
        else:
            self.cooldown = self.delay
        self._shoot(env, player, self.slash)

    def update(self):
        if self.cooldown:
            self.cooldown -= 1

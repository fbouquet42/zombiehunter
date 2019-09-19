from . import DefaultWeapon

class   MagicWand(DefaultWeapon):
    name = 'magic_wand'
    sonic_delay = 96
    magic_delay = 10

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_empty = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_empty', cls.dimensions)
        cls.img_full = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_full', cls.dimensions)
        cls.img_loading = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_loading', cls.dimensions)
        cls.img_power = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_power', cls.dimensions)

        env.mod.bullets.MagicBall.pre_build(env)
        env.mod.bullets.SonicBall.pre_build(env)

    def __init__(self, env, player):
        self.player = player

        self.full = True
        self.energy = 10

        self.magic = env.mod.bullets.MagicBall.build_class(env, player, self)
        self.sonic = env.mod.bullets.SonicBall.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.full:
            img = self.img_full[direction]
        elif self.energy > self.sonic_delay:
            img = self.img_power[direction]
        elif self.energy >= self.magic_delay:
            img = self.img_loading[direction]
        else:
            img = self.img_empty[direction]
        self.tools.display(env, img, x, y, fitting)

    def not_pressed(self, env, player):
        if self.full:
            pass
        elif self.energy >= self.magic_delay:
            if self.energy >= self.sonic_delay:
                self._shoot(env, player, self.sonic)
            self.energy = 0
        else:
            self.energy += 1
            if self.energy == self.magic_delay:
                self.full = True

    def pressed(self, env, player):
        if self.full:
            self._shoot(env, player, self.magic)
            self.energy = 0
            self.full = False
        else:
            self.energy += 1

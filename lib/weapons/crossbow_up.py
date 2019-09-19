from . import DefaultWeapon

class   CrossbowUp(DefaultWeapon):
    name = 'crossbow_tier2_unloaded'

    def __init__(self, env, player):
        self.tools = env.mod.tools
        self.dimensions = player.dimensions
        self.player = player
        env.jerk_fitting = 13

        self.loading = 0
        self.loaded = 13
        self.overloaded = 119

        self.img_unloaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_tier2_unloaded", self.dimensions)
        self.img_loaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_tier2_loaded", self.dimensions)
        self.img_overloaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_tier2_overloaded", self.dimensions)

        self.arrow = env.mod.bullets.ArrowUp.build_class(env, player, self)
        self.electric_arrow = env.mod.bullets.ElectricArrow.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.loading > self.overloaded:
            img = self.img_overloaded[direction]
        elif self.loading > self.loaded:
            img = self.img_loaded[direction]
        else:
            img = self.img_unloaded[direction]
        self.tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        self.loading += 1

    def not_pressed(self, env, player):
        if self.loading > self.overloaded:
            self._shoot(env, player, self.electric_arrow)
        elif self.loading > self.loaded:
            self._shoot(env, player, self.arrow)
        self.loading = 0

from . import DefaultWeapon

class   Crossbow(DefaultWeapon):
    def __init__(self, env, player):
        self.tools = env.mod.tools
        self.dimensions = player.dimensions

        self.loading = 0
        self.loaded = 13
        self.overloaded = 142

        self.img_unloaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_unloaded", self.dimensions)
        self.img_loaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_loaded", self.dimensions)
        self.img_overloaded = self.tools.set_imgs(env.img_folder + 'weapons/', "crossbow_overloaded", self.dimensions)

        self.arrow = env.mod.bullets.Arrow.build_class(env, player)
        self.rocket = env.mod.bullets.Rocket.build_class(env, player)

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
            self._shoot(env, player, self.rocket)
        elif self.loading > self.loaded:
            self._shoot(env, player, self.arrow)
        self.loading = 0

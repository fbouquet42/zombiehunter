from . import DefaultWeapon
from random import randint

class   ShadowDaggers(DefaultWeapon):
    name = 'shadow_daggers'
    tier_up = True

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_equipped', cls.dimensions)
        cls.img_empty = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_sent', cls.dimensions)
        cls.img_power = cls.tools.set_imgs(env.img_folder + 'weapons/', cls.name + '_power', cls.dimensions)

        env.mod.bullets.ShadowDaggers.pre_build(env)

    def __init__(self, env, player):
        self.player = player

        self.delay = 9
        self.cooldown = 0
        self.next_shadow = randint(1, 36)
        self.shadow = 0

        self.daggers = env.mod.bullets.ShadowDaggers.build_class(env, player, self)
        self.assassination = env.mod.bullets.Assassination(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.shadow:
            img = self.img_power[direction]
        elif self.cooldown:
            img = self.img_empty[direction]
        else:
            img = self.img[direction]
        self.tools.display(env, img, x, y, fitting)
    
    def _assassination(self):
        self.assassination.process()
        self.player.shadow = False
        self.next_shadow = randint(1, 36)

    def pressed(self, env, player):
        if self.shadow:
            self.shadow = 0
            self._assassination()
        elif not self.cooldown:
            self._shoot(env, player, self.daggers)
            self.next_shadow -= 1
            self.cooldown = self.delay
            if not self.next_shadow:
                self.player.shadow = True
                self.shadow = 60

    def update(self):
        if int(self.xp) > self.level_up:
            self.evolve()
        if self.shadow:
            self.shadow -= 1
            if not self.shadow:
                self._assassination()
        elif self.cooldown:
            self.cooldown -= 1

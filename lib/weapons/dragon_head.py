from . import DefaultWeapon
from threading import Thread
from random import randint

class   DragonHead(DefaultWeapon):
    name = 'dragon_head'

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_apnea = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_apnea', cls.dimensions)
        cls.img_breathe = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_breathe', cls.dimensions)
        cls.img_suffocate = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_suffocate', cls.dimensions)

        env.mod.bullets.FireTooth.pre_build(env)
        env.mod.bullets.Tooth.pre_build(env)

    def __init__(self, env, player):
        self.env = env
        self.player = player

        self.delay = 6
        self.cooldown = 0
        self.suffocating = 0
        self.breathing = False
        self.apnea = randint(4, 7)

        self.fire_tooth = env.mod.bullets.FireTooth.build_class(env, player, self)
        self.tooth = env.mod.bullets.Tooth.build_class(env, player, self)
        self.smoke_cloud = env.mod.bullets.SmokeCloud.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.breathing:
            img = self.img_breathe[direction]
        elif self.suffocating:
            img = self.img_suffocate[direction]
        else:
            img = self.img_apnea[direction]
        self.tools.display(env, img, x, y, fitting)

    def pressed(self, env, player):
        if self.cooldown or self.suffocating:
            return
        else:
            self.cooldown = self.delay
        if self.breathing:
            self._shoot(env, player, self.fire_tooth)
            self.suffocating = 36
            self.breathing = False
        else:
            self._shoot(env, player, self.tooth)
            self.apnea -= 1
            if not self.apnea:
                self.breathing = True
                self.apnea = randint(4, 7)

    def update(self):
        if self.cooldown:
            self.cooldown -= 1

        if self.suffocating:
            if not self.suffocating % 7:
                self._shoot(self.env, self.player, self.smoke_cloud)
            self.suffocating -= 1

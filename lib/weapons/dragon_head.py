from . import DefaultWeapon
from threading import Thread

class   DragonHead(DefaultWeapon):
    name = 'dragon_head'

    @classmethod
    def build_class(cls, env):
        cls.tools = env.mod.tools
        cls.dimensions = env.player_dimensions
        cls.img_apnea = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_apnea', cls.dimensions)
        cls.img_breathe = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_breathe', cls.dimensions)
        cls.img_sleep = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_sleep', cls.dimensions)

        env.mod.bullets.FireBall.pre_build(env)

    def __init__(self, env, player):
        self.env = env
        self.player = player

        self.delay = 6
        self.cooldown = 0
        self.suffocating_max = 99 * 2.5
        self.suffocating = self.suffocating_max
        self.breathing = 0
        self.sleeping = 0

        self.fire_ball = env.mod.bullets.FireBall.build_class(env, player, self)
        self.smoke_cloud = env.mod.bullets.SmokeCloud.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.breathing:
            img = self.img_breathe[direction]
        elif self.sleeping:
            img = self.img_sleep[direction]
        else:
            img = self.img_apnea[direction]
        self.tools.display(env, img, x, y, fitting)

######
    def pressed(self, env, player):
        if not self.sleeping and not self.breathing:
            self.suffocating -= 2.5
        if self.cooldown or self.sleeping:
            return
        if self.breathing:
            self.cooldown = 2
        else:
            self.cooldown = self.delay
        self._shoot(env, player, self.fire_ball)


    def update(self):
        if self.cooldown:
            self.cooldown -= 1

        if self.suffocating < self.suffocating_max:
            if self.suffocating < 0:
                self.breathing = 155
                self.suffocating = self.suffocating_max
            self.suffocating += 1

        if self.breathing:
            self.breathing -= 1
            if not self.breathing:
                self.sleeping = 101
                
        if self.sleeping:
            if not self.sleeping % 11:
                self._shoot(self.env, self.player, self.smoke_cloud)
            self.sleeping -= 1

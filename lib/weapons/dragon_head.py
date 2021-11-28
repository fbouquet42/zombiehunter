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
        cls.img_suffocate = cls.tools.set_imgs(env.img_folder + 'weapons/', 'dragon_head_suffocate', cls.dimensions)

        env.mod.bullets.FireTooth.pre_build(env)
        env.mod.bullets.Tooth.pre_build(env)

    def __init__(self, env, player):
        self.env = env
        self.player = player

        self.delay = 6
        self.cooldown = 0
        self.suffocating = 0
        self.release = False
        self.wants_to_breathe = 0
        self.breathing = 0

        self.fire_tooth = env.mod.bullets.FireTooth.build_class(env, player, self)
        self.tooth = env.mod.bullets.Tooth.build_class(env, player, self)
        self.smoke_cloud = env.mod.bullets.SmokeCloud.build_class(env, player, self)

    def display(self, env, direction, x, y, fitting):
        if self.breathing:
            img = self.img_breathe[direction]
        elif self.wants_to_breathe:
            img = self.img_suffocate[direction]
        else:
            img = self.img_apnea[direction]
        self.tools.display(env, img, x, y, fitting)

    def not_pressed(self, env, player):
        if self.suffocating:
            self.release = True

    #spam shoot to breathe
    def pressed(self, env, player):
        if self.suffocating and self.release:
            self.wants_to_breathe += 1
            self.suffocating = 0
            self.release = False
            self._shoot(self.env, self.player, self.smoke_cloud)
        if not self.breathing:
            self.suffocating = 5
        if self.cooldown:
            return
        else:
            self.cooldown = self.delay
        if self.breathing:
            self._shoot(env, player, self.fire_tooth)
        else:
            self._shoot(env, player, self.tooth)

    def update(self):
        if self.cooldown:
            self.cooldown -= 1

        if self.suffocating:
            self.suffocating -= 1
            if not self.suffocating:
                self.wants_to_breathe = 0
                self.release = False

        if self.wants_to_breathe > 4:
            self.breathing = 205
            self.wants_to_breathe = 0

        if self.breathing:
            self.breathing -= 1
            #if not self.breathing:
            #    self.sleeping = 101

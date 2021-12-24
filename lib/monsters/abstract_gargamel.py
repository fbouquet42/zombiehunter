from . import DefaultMonster
from . import Lamb

#2 phase, and sheep procession
class AbstractGargamel(DefaultMonster):
    name = "gargamel"
    degeneration = 550
    rapidity = 9
    attack = 3
    id_nb = 20

    @classmethod
    def build_class(cls):
        cls.dimensions = int(cls.dimensions * 3.25)
        cls.half = cls.dimensions // 2
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_hungry = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_hungry', cls.dimensions)
        cls.img_scimitar = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'scimitar', cls.dimensions)
        cls.img_spear = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'spear', cls.dimensions)
        cls.scimitar = cls.env.mod.objects.Scimitar.build_class(cls.env, cls.dimensions)
        cls.spear = cls.env.mod.objects.Spear.build_class(cls.env, cls.dimensions)

        cls.void = cls.env.mod.objects.Void.build_class(cls.env, cls.dimensions)

        cls.procession = cls.env.mod.bullets.LambsProcession.build_class(Lamb.build_class(cls.env))

        cls.title = cls.env.mod.tools.load_img(cls.env, 'waves/gargamel_will_be_back', cls.env.height, cls.env.height)

    def hitted(self, attack=1):
        if self.lives:
            self.injured = 14
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def recall(self, x, y):
        if not self.lives:
            return
        self.env.objects.append(self.void(self.x, self.y, expired=False))
        self.x = x
        self.y = y
        self.env.objects.append(self.void(self.x, self.y, expired=True))

    def set_on_fire(self, n, player):
        pass

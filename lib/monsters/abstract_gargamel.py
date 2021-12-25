from random import randint

from . import DefaultMonster
from . import Lamb

class GargamelWeapon(object):
    @classmethod
    def build_abstract(cls, env, dimensions):
        cls.env = env
        cls.tools = env.mod.tools
        cls.dimensions = dimensions

    @classmethod
    def set_monster(cls, monster):
        cls.monster = monster

    def _next_spell(self):
        self.spell = randint(self.mi, self.ma)
        
    def __init__(self, delay=0):
        self.free = False
        self.in_hand = True
        if not delay:
            self._next_spell()
        else:
            self.spell = delay

    def recall(self, x, y):
        self.free = True
        self.monster.recall(x, y)

    def _perform(self):
        pass

    def update(self):
        if self.spell:
            self.spell -= 1
            if not self.spell:
                self.in_hand = False
                self._perform()

class GargamelScimitar(GargamelWeapon):
    mi = 43
    ma = 72
    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'scimitar', cls.dimensions)
        cls.obj = cls.env.mod.objects.Scimitar.build_class(cls.env, cls.dimensions)
        return cls
    def _perform(self):
        self.env.objects.append(self.obj(self.monster.x, self.monster.y, self))

class GargamelNothing(GargamelWeapon):
    def __init__(self, other_hand):
        self.free = False
        self.in_hand = False
        self.other_hand = other_hand

    def update(self):
        if self.other_hand.free:
            self.free = True

class GargamelSpear(GargamelWeapon):
    mi = 66
    ma = 102
    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'spear', cls.dimensions)
        cls.obj = cls.env.mod.objects.Spear.build_class(cls.env, cls.dimensions)
        return cls
    def _perform(self):
        self.env.objects.append(self.obj(self.monster.x, self.monster.y, self))


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
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_hungry = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_hungry', cls.dimensions)
        cls.img_hungry_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_hungry_injured', cls.dimensions)

        GargamelWeapon.build_abstract(cls.env, cls.dimensions)
        cls.nothing = GargamelNothing
        cls.scimitar = GargamelScimitar.build_class()
        cls.spear = GargamelSpear.build_class()

        cls.void = cls.env.mod.objects.Void.build_class(cls.env, cls.dimensions)

        cls.procession = cls.env.mod.bullets.LambsProcession.build_class(Lamb.build_class(cls.env))

        cls.title = cls.env.mod.tools.load_img(cls.env, 'waves/gargamel_will_be_back', cls.env.height, cls.env.height)

    def set_dependencies(self):
        GargamelWeapon.set_monster(self)
        Lamb.set_gargamel(self)

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

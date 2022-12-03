from random import randint
from threading import Thread

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

    def protect(self, attack):
        return False

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

    def get_img(self):
        return self.img

    def _perform(self):
        pass

    def update(self):
        if self.spell:
            self.spell -= 1
            if not self.spell:
                self.in_hand = False
                self._perform()

class GargamelShield(GargamelWeapon):
    mi = 88
    ma = 132
    lives = 60
    injured = 0

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'shield', cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'shield_injured', cls.dimensions)
        cls.dead = cls.env.mod.objects.ShieldDead.build_class(cls.env, cls.dimensions)
        return cls

    def protect(self, attack):
        if self.lives <= 0:
            return False
        self.injured = 10
        self.lives -= attack
        if self.lives <= 0:
            self.in_hand = False
            self.env.objects.append(self.dead(self.monster))
        return True

    def get_img(self):
        if self.injured:
            return self.img_injured
        else:
            return self.img

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.in_hand and self.spell:
            self.spell -= 1
            if not self.spell:
                self.free = True
                self.env.objects.append(self.dead(self.monster))

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

class GargamelSceptre(GargamelWeapon):
    mi = 199
    ma = 299

    @classmethod
    def build_class(cls, obj, lamb):
        cls.obj = obj
        cls.img_off = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'sceptre_off', cls.dimensions)
        cls.img_on = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'sceptre', cls.dimensions)
        cls.invocations = cls.env.mod.bullets.LambsInvocation.build_class(lamb)
        return cls

    def __init__(self, delay=0):
        self.free = False
        self.in_hand = True
        if not delay:
            self._next_spell()
        else:
            self.spell = delay
        
        invoc = self.invocations(self, self.monster)
        t = Thread(target=invoc.spawn, args=())
        t.daemon = True
        self.env.bullets.append(invoc)
        t.start()
        self.spawned = 0

    def _perform(self):
        self.env.objects.append(self.obj(self.monster.x, self.monster.y, self))

    def get_img(self):
        if self.spawned:
            return self.img_on
        else:
            return self.img_off

    def update(self):
        if self.spawned:
            self.spawned -= 1
        if self.spell:
            self.spell -= 1
            if not self.spell:
                self.in_hand = False
                self._perform()

class GargamelCatch(GargamelWeapon):
    mi = 88
    ma = 132

    @classmethod
    def build_class(cls):
        cls.img_1 = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'lamb_shaking_1', cls.dimensions)
        cls.img_2 = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'lamb_shaking_2', cls.dimensions)
        cls.img_3 = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'lamb_shaking_3', cls.dimensions)
        cls.bullet = cls.env.mod.bullets.ThrowingLamb.build_class(cls.env, cls.dimensions)
        return cls

    def get_img(self):
        shaking = (self.spell % 9) // 3
        if not shaking:
            return self.img_1
        elif shaking == 1:
            return self.img_2
        else:
            return self.img_3

    def _perform(self):
        bullet = self.bullet(self.monster.x, self.monster.y, self.monster.direction, self)
        t = Thread(target=bullet.move, args=())
        t.daemon = True
        self.env.bullets.append(bullet)
        t.start()

class GargamelKnife(GargamelWeapon):
    mi = 88
    ma = 132

    @classmethod
    def build_class(cls):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'knife', cls.dimensions)
        cls.img_prepared = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'knife_throwing', cls.dimensions)
        cls.bullet = cls.env.mod.bullets.ThrowingKnife.build_class(cls.env, cls.dimensions)
        return cls

    def get_img(self):
        if self.spell < 33:
            return self.img_prepared
        else:
            return self.img

    def _perform(self):
        bullet = self.bullet(self.monster.x, self.monster.y, self.monster.direction, self)
        t = Thread(target=bullet.move, args=())
        t.daemon = True
        self.env.bullets.append(bullet)
        t.start()

class GargamelSpear(GargamelWeapon):
    mi = 84
    ma = 122
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


        cls.lamb = Lamb.build_class(cls.env)
        GargamelWeapon.build_abstract(cls.env, cls.dimensions)
        cls.nothing = GargamelNothing
        cls.scimitar = GargamelScimitar.build_class()
        cls.spear = GargamelSpear.build_class()
        cls.sceptre = GargamelSceptre.build_class(cls.spear.obj, cls.lamb)
        cls.shield = GargamelShield.build_class()
        cls.knife = GargamelKnife.build_class()

        cls.void = cls.env.mod.objects.Void.build_class(cls.env, cls.dimensions)

        cls.procession = cls.env.mod.bullets.LambsProcession.build_class(cls.lamb)

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

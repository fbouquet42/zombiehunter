
#Python Lib
from random import randint

#Current Module
from . import DefaultMonster
from . import Zombie
from . import set_hitbox_monster

class Vial:
    def __init__(self, img, effect):
        self.img = img
        self.effect = effect

class Alchemist(DefaultMonster):
    lives = 50
    name = "alchemist"
    id_nb = 15
    potion_effect = False

    @classmethod
    def build_class(cls, env):
        cls.img = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name, cls.dimensions)
        cls.img_injured = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_injured', cls.dimensions)
        cls.img_dead = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_dead', cls.dimensions)
        cls.img_possessed = cls.tools.set_imgs(cls.env.img_folder + 'monsters/', cls.name + '_possessed', cls.dimensions)
        cls.img_fog = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'fog_vial', cls.dimensions)
        cls.img_invulnerable = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'invulnerable_vial', cls.dimensions)
        cls.img_summoning = cls.tools.set_imgs(cls.env.img_folder + 'weapons/', 'summoning_vial', cls.dimensions)
        cls.fog_class = env.mod.objects.Fog.build_class(env)
        cls.fog_vial = Vial(cls.img_fog, cls.fog_class)
        cls.summoning_class = env.mod.objects.SummoningVial.build_class(env, Zombie)
        cls.summoning_vial = Vial(cls.img_summoning, cls.summoning_class)
        cls.invulnerable_class = env.mod.objects.InvulnerableVial.build_class(env)
        cls.invulnerable_vial = Vial(cls.img_invulnerable, cls.invulnerable_class)
        cls.vials = [cls.fog_vial, cls.invulnerable_vial, cls.summoning_vial]
        return cls


    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.env = env
        self.hitbox = set_hitbox_monster(env, self)

        self.rapidity = randint(6, 9)

        self.vial = None
        self.spelling = 0
        self.next_vial = randint(140, 275)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.vial is not None :
            self.tools.display(self.env, self.vial.img[self.direction], self.x, self.y, fitting)
        self._debug()

    def update(self):
        if self.stoned and not self.env.stoned:
            self.stoned = False
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if not self.lives or self.stoned:
            if not self.lives and self.vial:
                self.env.objects.insert(0, self.vial.effect(self.x, self.y))
                self.vial = None
            pass
        elif self.spelling:
            self.spelling -= 1
            if not self.spelling:
                self.env.objects.insert(0, self.vial.effect(self.x, self.y))
                self.next_vial = randint(140, 275)
                self.vial = None
        else:
            self.next_vial -= 1
            if not self.next_vial:
                self.spelling = 44
                self.vial = self.vials[randint(0, len(self.vials) - 1)]

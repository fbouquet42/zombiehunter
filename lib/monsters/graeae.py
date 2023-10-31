from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Pestilence
from . import Deino
from . import Enyo
from . import Pemphredo

#wand with diamonds and bolts ? explodes on hit ? tempests ? cloud ? turning aoe ? multiple shot ? more effect on electricity ? heal ?
#deino -> enyo -> pemphredo ? phase avec immunite ?
#taille de baguettes qui grossit ?
#pluie de one shot ?
#pattern pour esquiver a la space invader ? horloge ?
#main qui s arrache ?

class Graeae(DefaultMonster):
    name = "graeae"
    degeneration = 150
    lives = 10 #how much ?
    rapidity = 7
    attack = 3
    id_nb = 19
    splited_lives = 3

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
#        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)

        self.cloud_spawner = env.mod.objects.CloudSpawner.build_class(env)
        self.bolt = env.mod.bullets.Bolt.build_class(env)
        self.skull = env.mod.bullets.LightingSkull.build_class(env)
        self.blood = env.mod.objects.Blood.build_class(env, self.dimensions)
        self.pestilence = Pestilence.build_class(env)
        self.spelling = False
        self.splited = [Deino.build_class(env), Enyo.build_class(env), Pemphredo.build_class(env)]
        #self.next_spell()
        #self.spell_type = [self.fire_spell , self.star_spell]

        self.sweat = 60
        self.hitbox = set_hitbox_monster(env, self, 0.7)
        self.next_spell()
        self.spells = [self.throw_bolt, self.throw_skull]

        env.objects.append(self.cloud_spawner(self))

    def throw_skull(self):
        skull = self.skull(self.x, self.y, self.direction)
        t = Thread(target=skull.move, args=())
        t.daemon = True
        self.env.bullets.append(skull)
        t.start()

    def throw_bolt(self):
        bolt = self.bolt(self.x, self.y, self.direction)
        t = Thread(target=bolt.move, args=())
        t.daemon = True
        self.env.bullets.append(bolt)
        t.start()

    def next_spell(self):
        self.will_spell = randint(130, 220)

    def hitted(self, attack=1):
        if self.lives and not self.spelling:
            self.injured = 14
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            direction, _ = self._sniff_fresh_flesh()
            if direction is not None:
                self.direction = direction
                if not self.spelling:
                    self.tools.move(self, direction, self.rapidity)
                    self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return
        self.env.objects.append(self.blood(self.x, self.y))
        for monster_type in self.splited:
            monster = monster_type(self, self.x, self.y)
            t = Thread(target=monster.move, args=())
            t.daemon = True
            self.env.monsters.append(monster)
            t.start()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            img = self.img_dead[self.direction]
        #elif self.spelling:
        #    img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        self._debug()

    def update(self):
        super().update()

        if self.lives:
            self.sweat -= 1
            if not self.sweat:
                p = self.pestilence(self.x, self.y, self.direction)
                t = Thread(target=p.drip, args=())
                t.daemon = True
                self.env.monsters.insert(0, p)
                t.start()
                self.sweat = 20
            self.will_spell -= 1
            if not self.will_spell:
                self.spells[randint(0, len(self.spells) - 1)]()
                self.next_spell()

    def set_on_fire(self, n, player):
        pass

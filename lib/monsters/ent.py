from threading import Thread
from random import randint
import time

from . import DefaultMonster
from . import set_hitbox_monster

class   Ent(DefaultMonster):
    name = "ent"
    lives = 330
    id_nb = 7
    attack = 2
    max_thorny = 30
    nb_thorns = 3
    forest = True
    degeneration = 550

    def build_class():
        Ent.img = Ent.tools.set_imgs(Ent.env.img_folder + 'monsters/', Ent.name, Ent.dimensions)
        Ent.img_injured = Ent.tools.set_imgs(Ent.env.img_folder + 'monsters/', Ent.name + '_injured', Ent.dimensions)
        Ent.img_spelling = Ent.tools.set_imgs(Ent.env.img_folder + 'monsters/', Ent.name + '_spelling', Ent.dimensions)
        Ent.img_dead = Ent.tools.set_imgs(Ent.env.img_folder + 'monsters/', Ent.name + '_dead', Ent.dimensions)
        Ent.img_possessed = Ent.tools.set_imgs(Ent.env.img_folder + 'monsters/', Ent.name + '_possessed', Ent.dimensions)
        Ent.thorns = Ent.env.mod.bullets.Thorns.build_class(Ent.env)
        Ent.vines = Ent.env.mod.monsters.Vines.build_class()
        Ent.brambles = Ent.env.mod.monsters.Brambles.build_class(Ent.env)
        return Ent

    def next_spell(self):
        self.spell = randint(155, 340)

    def __init__(self, env, x, y):
        self._father_init(x, y)
        self.hitbox = set_hitbox_monster(env, self, 0.48)

        self.rapidity = randint(7, 8)

        self.thorny = 0
        self.cradling = 0
        self.spelling = False
        self.next_spell()
        self.spell_type = [self.thorns_spell, self.brambles_wall_spell, self.vines_spell, self.brambles_circle_spell]

    def brambles_circle_spell(self):
        self.cradling = 16
        for i in range(0, 8):
            circle = self.brambles(self, 0, direction=i)
            t = Thread(target=circle.move, args=())
            t.daemon = True
            self.env.monsters.append(circle)
            t.start()

    def brambles_wall_spell(self):
        self.cradling = 40
        wall = self.brambles(self, 10)
        t = Thread(target=wall.move, args=())
        t.daemon = True
        self.env.monsters.append(wall)
        t.start()

    def vines_spell(self):
        self.cradling = 35
        if self.target is not None:
            vines = self.vines(self, self.target)
            t = Thread(target=vines.move, args=())
            t.daemon = True
            self.env.monsters.append(vines)
            t.start()

    def thorns_spell(self):
        if not self.thorny:
            self.thorny = self.max_thorny
        timer = (self.max_thorny - self.thorny) // 2
        if self.target is not None:
            thorns = self.thorns(self.target.x, self.target.y, self.direction, self, timer)
            t = Thread(target=thorns.explose, args=())
            t.daemon = True
            self.env.bullets.append(thorns)
            t.start()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.spelling:
            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        if self.lives and self.invulnerable:
            self.tools.display(self.env, self.img_invulnerable_large[self.direction], self.x, self.y, fitting)
        elif self.lives and self.inflamed:
            self.tools.display(self.env, self.img_inflamed_large[self.direction], self.x, self.y, fitting)
        self._debug()

    def hitted(self, attack=1):
        if self.invulnerable:
            return None, None
        if self.lives and not self.spelling:
            self.injured = 12
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            if not self.stoned:
                direction, _ = self._sniff_fresh_flesh()
                if direction is not None:
                    self.direction = direction
                    if not self.spelling:
                        self.tools.move(self, direction, self.rapidity + self.env.furious)
                        self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
            if self._quit():
                return

    def update(self):
        if self.invulnerable:
            self.invulnerable -= 1
        if self.stoned and not self.env.stoned:
            self.stoned = False
            if self.spelling:
                self.cradling = 0
                self.thorny = 0
                self.spelling = False
                self.spell = randint(80, 380)
        if self.injured:
            self.injured -= 1
        self._perform_fire()
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if not self.lives or self.stoned:
            pass
        elif self.cradling:
            self.cradling -= 1
            if not self.cradling:
                self.spelling = False
        elif self.thorny:
            self.thorny -= 1
            if not self.thorny:
                self.spelling = False
            elif not self.thorny % (self.max_thorny // self.nb_thorns):
                self.thorns_spell()
        elif self.spell:
            self.spell -= 1
            if not self.spell:
                self.spelling = True
                self.spell_type[randint(0, len(self.spell_type) - 1)]()
                self.next_spell()

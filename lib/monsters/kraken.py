from random import randint
from threading import Thread
import time

from . import DefaultMonster
from . import set_hitbox_monster
from . import Tentacle
from . import BaseTentacles
from . import Vortex

class Kraken(DefaultMonster):
    name = "kraken"
    lives = 1710
    #450 570 690
    # + 3 necromancer spawns
    rapidity = 4
    attack = 3
    id_nb = 8
    degeneration = 550
    rooted = True

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
        self.img_possessed = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_possessed', self.dimensions)

        self.hitbox = set_hitbox_monster(env, self, 0.7)
        Tentacle.build_class()
        Vortex.build_class(self.env, self)
        self.tentacles_headers = []
        for i in range(1, 5):
            self.tentacles_headers.append(BaseTentacles(env, self, i))

        self.spelling = 0
        self._next_spell()
        self.spell_type = [self.sporing]

        self.next_enlargement()

    def _next_spell(self):
        self.spell = randint(400, 630)

    def sporing(self):
        for tentacles_header in self.tentacles_headers:
            tentacles_header.spore_popping()

    def next_enlargement(self):
        self.expand = randint(100, 230)

    def growing(self):
        for tentacles_header in self.tentacles_headers:
            tentacles_header.growing()

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
#        elif self.furious:
#            img = self.img_furious[self.direction]
#        elif self.spelling:
#            img = self.img_spelling[self.direction]
        elif self.spelling:
            img = self.img_spelling[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)
        self._debug()

    def hitted(self, attack=1):
        if self.lives and not self.spelling:
            self.injured = 12
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_nb, attack
        return None, None

    def _action(self):
        direction, _ = self._sniff_fresh_flesh()
        if direction is not None:
            self.direction = direction
            if not self.spelling:
                self.tools.move(self, direction, self.rapidity + self.env.furious)
            self.hitbox.update_coords(self)
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        while self.lives:
            self._action()
            for tentacles_header in self.tentacles_headers:
                tentacles_header.update()
            if self._quit():
                return

        while self.degeneration:
            if self.env.walking_dead:
                self._action()
                for tentacles_header in self.tentacles_headers:
                    tentacles_header.update()
            if self._quit():
                return

    def update(self):
        if self.injured:
            self.injured -= 1
        if not self.lives and self.degeneration:
            self.degeneration -= 1
        if self.lives and self.poisoned:
            self.poisoned -= 1
            if not self.poisoned % 20:
                self.lives -= 1
                self.injured += 5
        if not self.lives:
            pass
        elif self.expand:
            self.expand -= 1
        else:
            self.growing()
            self.next_enlargement()
        if not self.lives:
            pass
        elif self.spelling:
            self.spelling -= 1
        else:
            self.spell -= 1
            if not self.spell:
                self.spell_type[randint(0, len(self.spell_type) - 1)]()
                self.spelling = randint(90, 115)
                self._next_spell()
                vortex = Vortex(self.x, self.y)
                t = Thread(target=vortex.update, args=())
                t.daemon = True
                t.start()

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
    name_nyx = "nyx"
    lives = 477
    lives_nyx = 700
    #500 300 700
    # + 3 necromancer spawns
    rapidity_kraken = 4
    rapidity = 9
    attack = 2
    id_kraken = 11
    id_nyx = 8
    degeneration = 550
    rooted = True
    huge = False
    transforming = 0
    night = 0

    def _kraken(self):
        self.env.night = False
        self.env.background = self.env.background_shadows
        self._next_spell()
        self.rapidity = self.rapidity_kraken
        self.huge = True
        self.hitbox = set_hitbox_monster(self.env, self, 0.7)
        for i in range(1, 5):
            self.tentacles_headers.append(BaseTentacles(self.env, self, i))
        self.spell_type = [self.sporing, self.spawning]

    def __init__(self, env, x, y):
        self._father_init(x, y)

        self.img = self.tools.set_imgs(env.img_folder + 'monsters/', self.name, self.dimensions)
        self.img_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_injured', self.dimensions)
        self.img_spelling = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_spelling', self.dimensions)
        self.img_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_dead', self.dimensions)
        self.img_possessed = self.tools.set_imgs(env.img_folder + 'monsters/', self.name + '_possessed', self.dimensions)
        self.img_nyx = self.tools.set_imgs(env.img_folder + 'monsters/', self.name_nyx, self.dimensions)
        self.img_nyx_injured = self.tools.set_imgs(env.img_folder + 'monsters/', self.name_nyx + '_injured', self.dimensions)
        self.img_nyx_night = self.tools.set_imgs(env.img_folder + 'monsters/', self.name_nyx + '_night', self.dimensions)
        self.img_nyx_injured_night = self.tools.set_imgs(env.img_folder + 'monsters/', self.name_nyx + '_injured_night', self.dimensions)
        self.img_nyx_dead = self.tools.set_imgs(env.img_folder + 'monsters/', self.name_nyx + '_dead', self.dimensions)

        self.hitbox = set_hitbox_monster(env, self)
        self.bullet = env.mod.bullets.JellyFish.build_class(Tentacle.env)
        Tentacle.build_class()
        Vortex.build_class(self.env, self)
        self.tentacles_headers = []

        self.spelling = 0
        self._next_spell_nyx()
        self.next_enlargement()

    def _next_spell(self):
        self.spell = randint(420, 640)

    def _next_spell_nyx(self):
        self.spell = randint(105, 170)

    def spawning(self):
        spawned = randint(4, 6)
        self.env.mod.tools.spawn(self.env, self.env.mod.monsters.Piranha, spawned)

    def sporing(self):
        for tentacles_header in self.tentacles_headers:
            tentacles_header.spore_popping()

    def next_enlargement(self):
        self.expand = randint(400, 490)

    def growing(self):
        for tentacles_header in self.tentacles_headers:
            tentacles_header.growing()

    def _display_kraken(self, env, fitting):
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
        self.tools.display(env, img, self.x, self.y, fitting)

    def _display_wizard(self, env, fitting):
        if not self.lives_nyx:
            img = self.img_nyx_dead[self.direction]
        elif self.injured:
            if self.night:
                img = self.img_nyx_injured_night[self.direction]
            else:
                img = self.img_nyx_injured[self.direction]
        else:
            if self.night:
                img = self.img_nyx_night[self.direction]
            else:
                img = self.img_nyx[self.direction]
        self.tools.display(env, img, self.x, self.y, fitting)

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if self.huge:
            self._display_kraken(env, fitting)
        else:
            self._display_wizard(env, fitting)
        self._debug()

    def affected(self, bullet):
        if self.transforming:
            return False
        if self.hitbox.x <= (bullet.hitbox.x + bullet.hitbox.dimensions) and bullet.hitbox.x <= (self.hitbox.x + self.hitbox.dimensions) and self.hitbox.y <= (bullet.hitbox.y + bullet.hitbox.dimensions) and bullet.hitbox.y <= (self.hitbox.y + self.hitbox.dimensions):
            return True
        return False

    def _dark_power(self):
        self.night = 450
        self.env.background = self.env.background_night
        self.env.night = True

    def _hitted_wizard(self, attack):
        self.injured = 12
        if self.lives_nyx > 300 and self.lives_nyx - attack <= 300:
            self._dark_power()
        elif self.lives_nyx > 600 and self.lives_nyx - attack <= 600:
            self._dark_power()
        self.lives_nyx -= attack
        self.lives_nyx = 0 if self.lives_nyx < 0 else self.lives_nyx
        return self.id_nyx, attack

    def hitted(self, attack=1):
        if not self.huge:
            return self._hitted_wizard(attack)
        if self.lives and not self.spelling:
            self.injured = 12
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            return self.id_kraken, attack
        return None, None

    def _action(self):
        direction, _ = self._sniff_fresh_flesh()
        if direction is not None:
            self.direction = direction
            if not self.spelling and not self.transforming:
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

    def _update_kraken(self):
        if not self.lives:
            return
        if self.expand:
            self.expand -= 1
        else:
            self.growing()
            self.next_enlargement()
        if self.spelling:
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

    def _update_wizard(self):
        if self.night:
            self.night -= 1
            if not self.night:
                self.env.night = False
                self.env.background = self.env.background_shadows
        if not self.lives_nyx and self.transforming:
            self.transforming -= 1
            if not self.transforming:
                self._kraken()
        elif not self.lives_nyx:
            self.env.night = False
            self.transforming = 50
        else:
            self.spell -= 1
            if not self.spell:
                bullet = self.bullet(self.x, self.y, self.direction, self)
                t = Thread(target=bullet.move, args=())
                t.daemon = True
                self.env.bullets.append(bullet)
                t.start()
                self._next_spell_nyx()

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
        if self.huge:
            self._update_kraken()
        else:
            self._update_wizard()

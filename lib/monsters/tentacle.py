
#Python Lib
from random import randint
from threading import Thread

#Current Module
from . import DefaultMonster
from . import set_hitbox_monster


class Tentacle(DefaultMonster):
    lives = 40
    name = "tentacle"
    id_nb = 9
    following = False
    degeneration = 200
    spore = False
    rooted = True

    def build_class():
        Tentacle.img = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name, Tentacle.dimensions)
        Tentacle.img_injured = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name + '_injured', Tentacle.dimensions)
        Tentacle.img_dead = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name + '_dead', Tentacle.dimensions)
        Tentacle.img_spore = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name + '_spore', Tentacle.dimensions)
        Tentacle.img_spore_injured = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name + '_spore_injured', Tentacle.dimensions)
        Tentacle.img_possessed = Tentacle.tools.set_imgs(Tentacle.env.img_folder + 'monsters/', Tentacle.name + '_possessed', Tentacle.dimensions)
        Tentacle.bullet = Tentacle.env.mod.bullets.JellyFish

    def __init__(self, env, monster, base, x, y, identity):
        self.x = x
        self.y = y
        self.hitbox = set_hitbox_monster(env, self)
        self.id = identity
        self.limit_coords = int(identity * 0.12 * self.dimensions)
        self.base = base
        self.monster = monster
        self.loading()

        self.target = self.base.target
        class _TestCoords:
            rapidity = 4
        self.test = _TestCoords
        self.test.x = x
        self.test.y = y
        self.test.rapidity += identity

    def loading(self):
        self.sporing = randint(75, 115)

    def hitted(self, attack=1):
        if self.lives:
            self.injured = self.injured_gradient
            self.lives -= attack
            self.lives = 0 if self.lives < 0 else self.lives
            if not self.lives:
                return self.id_nb, len(self.base.tentacles) - self.id
        return None, None

    def _limits(self):
        if self.test.x > self.base.x + self.limit_coords:
            self.x = self.base.x + self.limit_coords
        elif self.test.x < self.base.x - self.limit_coords:
            self.x = self.base.x - self.limit_coords
        else:
            self.x = self.test.x
        if self.test.y > self.base.y + self.limit_coords:
            self.y = self.base.y + self.limit_coords
        elif self.test.y < self.base.y - self.limit_coords:
            self.y = self.base.y - self.limit_coords
        else:
            self.y = self.test.y
        self.test.x = self.x
        self.test.y = self.y

    def _crawler(self):
        if self.lives or not self.stoned:
            x, y, distance = self.tools.process_distance(self.target, self)
            if distance > self.hitbox.dimensions:
                direction = self._determine_direction(x, y)
                self.direction = direction
                self.tools.force_move(self, x, y, self.direction, rapidity = distance - self.hitbox.dimensions)
            self.hitbox.update_coords(self)
        self._target_hitted()

    def move(self):
        self.tick = self.env.mod.tools.Tick()
        direction = None
        while self.lives:
            if not self.following:
                self.target = self.base.target
            elif not self.target.lives:
                self.following = False
                continue
            else:
                self.test.rapidity = self.target.test.rapidity
            x, y, _ = self.tools.process_distance(self.target, self)
            direction = self._determine_direction(x, y)
            self.direction = direction
            self.tools.force_move(self.test, x, y, self.direction)
            self._limits()
            self.hitbox.update_coords(self)
            self._target_hitted()
            if self._quit():
                return
            if not self.monster.lives:
                self.lives = 0

        if self.following:
            self.target.lives = 0
        self.rooted = False
        self.rapidity = 11
        while self.degeneration:
            if self.env.walking_dead:
                if not self.following:
                    self._action()
                else:
                    self._crawler()
            if self._quit():
                return

    def display(self, env):
        fitting = 0.23 * self.dimensions if self.direction % 2 else 0
        if not self.lives:
            if self.env.walking_dead and not self.following:
                img = self.img_possessed[self.direction]
            else:
                img = self.img_dead[self.direction]
        elif self.spore and self.injured:
            img = self.img_spore_injured[self.direction]
        elif self.spore:
            img = self.img_spore[self.direction]
        elif self.injured:
            img = self.img_injured[self.direction]
        else:
            img = self.img[self.direction]
        self.tools.display(self.env, img, self.x, self.y, fitting)
        self._debug()

    def set_on_fire(self, n, player):
        pass

    def update(self):
        super().update()
        if self.lives and self.spore:
            self.sporing -= 1
            if not self.sporing:
                bullet = self.bullet(self.x, self.y, self.direction, self)
                t = Thread(target=bullet.move, args=())
                t.daemon = True
                self.env.bullets.append(bullet)
                t.start()
                self.loading()
